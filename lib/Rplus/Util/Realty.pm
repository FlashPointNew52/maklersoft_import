package Rplus::Util::Realty;

use Rplus::Modern;
use utf8;
use Rplus::Model::Result;
use Rplus::Model::Result::Manager;
use JSON;
use Data::Dumper;
use Search::Elasticsearch;
use Rplus::Util::Geo;
use Exporter qw(import);
use Mojo::Util qw(trim);

our @EXPORT_OK = qw(save_data_to_all);

my $parser = DateTime::Format::Strptime->new( pattern => '%FT%T' );
my $parser_tz = DateTime::Format::Strptime->new( pattern => '%FT%T%z' );
my $media_name;
my $location;

sub save_data_to_all {
    my ($data, $mn, $loc) = @_;
    my $id;
    unless ($data->{add_date}) {
        my $dt = DateTime->now();
        $data->{add_date} = $dt->datetime();
    }
    while(my ($k,$v)=each(%$data)) {
        $v = trim($v);
        $v =~ s/^\n{1,}//i;
        $v =~ s/\n{1,}$//i;
    }
    $id = Rplus::Model::Result->new(metadata => to_json($data), media => $mn, location => $loc)->save;
    if ($data->{address}) {
        #say 'has address ' . $data->{address};
        my %coords = Rplus::Util::Geo::get_coords_by_addr($data->{locality}, $data->{address}, $data->{house_num});
        if (%coords) {
            $data->{location_lat} = $coords{latitude};
            $data->{location_lon} = $coords{longitude};
            $data->{location} = {"lat" => $data->{location_lat},"lon"=> $data->{location_lon}};
        }
        my $q = '';
        if ($data->{locality}) {
            $q .= $data->{locality};
        }
        if ($data->{address}) {
            $q .= ' ' . $data->{address};
        }

        if ($data->{house_num}) {
            $q .= ' ' . $data->{house_num};
        }

        $data->{tags} = $q;
        #say 'coords ' . $data->{location_lat}. ' ,' . $data->{location_lon};
    }
    foreach (@{$data->{owner_phones}}){
        $_ =~ s/\+|\(|\)|-|\s//g;
    }
    my $e = Search::Elasticsearch->new(nodes => 'import.rplusmgmt.com:9200');
    $e->index(
        index   => 'rplus-import',
        type    => 'offer',
        body    => {
            %$data
        }
    );

    say Dumper $data;

    return $id;
    # my $results = $e->search(
    #     index => 'rplus-import',
    #     body  => {
    #         query => {
    #             match_all => {}
    #         }
    #     }
    # );
    # return $data->render(json => $results);
}

sub put_object {
    my ($data, $mn, $loc) = @_;
    $media_name = $mn;
    $location =$loc;
    my $id;
    my @realtys = @{_find_similar(%$data)};


    if (scalar @realtys > 0) {
        foreach (@realtys) {
            $id = $_->id;   # что если похожий объект не один? какой id возвращать?
            my $o_realty = $_;
            say "Found similar realty: $id";

            my @phones = ();
            foreach (@{$o_realty->{metadata}->owner_phones}) {
                push @phones, $_;
            }

            if ($data->{add_date}) {
                $o_realty->{metadata}->last_seen_date($data->{add_date});
            } else {
                $o_realty->{metadata}->last_seen_date('now()');
            }
            $o_realty->{metadata}->change_date('now()');

            if ($o_realty->{metadata}->state_code ne 'work') {
                my @fields = qw(type_code source_media_id source_url source_media_text locality address house_num owner_price ap_scheme_id rooms_offer_count rooms_count condition_id room_scheme_id house_type_id floors_count floor square_total square_living square_kitchen square_land square_land_type);
                foreach (@fields) {
                    $o_realty->{metadata}->$_($data->{$_}) if $data->{$_};
                }
            }


            $o_realty->save(changes_only => 1);
            say "updated realty: ". $id;
        }
    } else {

        unless ($data->{add_date}) {
            my $dt = DateTime->now();
            $data->{add_date} = $dt->datetime();
        }

        $id = Rplus::Model::Result->new(metadata => to_json($data), media => $media_name, location => $location)->save;

        say "Saved new realty:". $id;
    }
}

sub _find_similar {
    my %data = @_;

    #
    # Универсальное правило
    # Совпадение: один из номеров телефонов + проверка по остальным параметрам
    #
    say 'is find';
    sleep(10);
    if (ref($data{'owner_phones'}) eq 'ARRAY' && @{$data{'owner_phones'}}) {

        my $realty = Rplus::Model::Result::Manager->get_objects(
            #select => 'id',
            query => [
                metadata => {
                    ltree_ancestor => to_json(
                        {
                            type_code=> $data{'type_code'},
                            offer_type_code=> $data{'offer_type_code'},
                            address=> $data{'address'},
                            house_num=> $data{'house_num'},
                            address=> $data{'address'},
                            \("owner_phones && '{".join(',', map { '"'.$_.'"' } @{$data{'owner_phones'}})."}'"),
                        }
                    )
                },

                #     ($data{'ap_num'} ? (OR => [ap_num => $data{'ap_num'}, ap_num => undef]) : ()),
                #     ($data{'rooms_count'} ? (OR => [rooms_count => $data{'rooms_count'}, rooms_count => undef]) : ()),
                #     ($data{'rooms_offer_count'} ? (OR => [rooms_offer_count => $data{'rooms_offer_count'}, rooms_offer_count => undef]) : ()),
                #     ($data{'floor'} ? (OR => [floor => $data{'floor'}, floor => undef]) : ()),
                #     ($data{'floors_count'} ? (OR => [floors_count => $data{'floors_count'}, floors_count => undef]) : ()),
                #     ($data{'square_total'} ? (OR => [square_total => $data{'square_total'}, square_total => undef]) : ()),
                #     ($data{'square_living'} ? (OR => [square_living => $data{'square_living'}, square_living => undef]) : ()),
                #     ($data{'square_land'} ? (OR => [square_land => $data{'square_land'}, square_land => undef]) : ()),
                # },
            media => $media_name,
            location => $location
            ],
            limit => 10,
        );

        return $realty if scalar @{$realty} > 0;
    }

    return [];
}

1;
