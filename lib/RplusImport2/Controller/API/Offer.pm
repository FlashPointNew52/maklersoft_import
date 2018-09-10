package RplusImport2::Controller::API::Offer;
use Mojo::Base 'Mojolicious::Controller';
use utf8;
use Rplus::DB;
use Rplus::Model::Result::Manager;
use Search::Elasticsearch;
use Data::Dumper;
use Mojo::Util qw(trim);

# Search:

my %type_codes = (
        "комната" => "room",
        "квартира" => "apartment",
        "малосемейка" => "apartment_small",
        "новостройка" => "apartment_new",
        "дом"  => "house" ,

        "дача" => "dacha",
        "коттедж" => "cottage",

        "таунхаус" => "townhouse",

        "другое" => "other",
        "земля" => "land",

        "здание" => "building",
        "офис" => "office_place, office",
        "торговая площадь" => "market_place",
        "производственное помещение" => "production_place",
        "помещение общего назначения" => "gpurpose_place",
        "автосервис" => "autoservice_place",
        "помещение под сферу услуг" => "service_place",
        "склад база" => "warehouse_place",
        "гараж" => "garage",
);

my %source_media = (
        "авито" => "avito",
        "из рук в руки" => "irr",
        "презент" => "present_site",
        "фарпост" => "farpost",
        "циан"  => "cian"
);

sub search {
    my $self = shift;

    my $query = $self->param('query') || '';
    my $offer_type = $self->param('offer_type') || 0;
    my $change_date = $self->param('change_date');
    my $page = $self->param('page') || 0;
    my $per_page = $self->param('per_page') || 50;
    my $search_area = $self->param('search_area') || 0;
    my $agent = $self->param('agent') || '';
    my $sort = $self->param('sort') || '';

    my %full_query = (
        index => 'rplus-import',
        type => 'offer',
        body  => {
            query => {
                bool => {
                    must => []
                }
            },
            sort => [],
            size  => $per_page,
            from => $per_page * $page
        }
    );

    if($offer_type){
        push(
             @{$full_query{body}{query}{bool}{must}},
             {
                "term"  => {
                    offer_type_code => $offer_type
                }
            }
         );
    }

    if($search_area && scalar $search_area){
        $search_area =~ s/\[|\]|\{|\}|\"//g;
        my @area;
        while($search_area =~ /(lat:(\d+\.\d+)\,lon:(\d+\.\d+))/){
            if($2 && $3){
                push(@area,{lat =>$2, lon=>$3});
            }
            $search_area =~ s/$1//i;
        }

        $full_query{body}{query}{bool}{filter}{geo_polygon} =
        {
            location => {
                points => \@area
            }
        };
    }

    if($agent eq 'private'){
        push(
            @{$full_query{body}{query}{bool}{must_not}},
            {
                exists => {
                    field =>  "mediator_company"
                }
            }
        );
    } elsif($agent =~ /realtor (.{1,})/){
        my $content_phones = '';
        my $phones_str = $1;
        while($phones_str =~ /((7|8){0,1}(\d{10}))|(7\s{0,1}\((\d{3,4})\)\s{0,1}(\d{2,3})-(\d{2})-(\d{2}))/){
            if($5 && $6 && $7 && $8){
                $content_phones = $content_phones.'7'.$5.$6.$7.$8.'|';
                $phones_str =~ s/7\s{0,1}\(($5)\)\s{0,1}$6-$7-$8//i;
            } else {
                $content_phones = $content_phones.'7'.$3.'|';
                $phones_str =~ s/$1//i;
            }
        }
        $content_phones =~ s/\|$//g;
        push(
             @{$full_query{body}{query}{bool}{must}},
             {
                "bool" => {
                    "minimum_should_match" => 1,
                    "should" => [
                        { "regexp" => {
                            "owner_phones" => $content_phones
                            }
                        },
                        {
                            "exists" => {
                                "field" => "mediator_company"
                            }
                        }

                     ],
                }
            }
        );
    } elsif($agent =~ /phones (.{1,})/){
        my $content_phones = '';
        my $phones_str = $1;
        while($phones_str =~ /((7|8){0,1}(\d{10}))|(7\s{0,1}\((\d{3,4})\)\s{0,1}(\d{2,3})-(\d{2})-(\d{2}))/){
            if($5 && $6 && $7 && $8){
                $content_phones = $content_phones.'7'.$5.$6.$7.$8.'|';
                $phones_str =~ s/7\s{0,1}\(($5)\)\s{0,1}$6-$7-$8//i;
            } else {
                $content_phones = $content_phones.'7'.$3.'|';
                $phones_str =~ s/$1//i;
            }
        }
        $content_phones =~ s/\|$//g;
        push(
             @{$full_query{body}{query}{bool}{must}},
             {
                "bool" => {
                    "minimum_should_match" => 1,
                    "should" => [
                        { "regexp" => {
                            "owner_phones" => $content_phones
                            }
                        }
                     ],
                }
            }
        );
    }

    foreach (keys %type_codes) {
         if($query =~/$_/){
             push(
                 @{$full_query{body}{query}{bool}{must}},
                 {
                     term => {
                         type_code =>  $type_codes{$_}
                     }
                 }
             );
             $query =~ s/$_//i;
         }
    }

    foreach (keys %source_media) {
         if($query =~/$_/){
             push(
                 @{$full_query{body}{query}{bool}{must}},
                 {
                     term => {
                         source_media =>  $source_media{$_}
                     }
                 }
             );
             $query =~ s/$_//i;
         }
    }
    my $content_phones = ''; #+7 (924) 404-28-80 +7 (4212) 94-14-01
    while($query =~ /((7|8){0,1}(\d{10}))|(7\s{0,1}\((\d{3,4})\)\s{0,1}(\d{2,3})-(\d{2})-(\d{2}))/){
        if($5 && $6 && $7 && $8){
            $content_phones = $content_phones.'7'.$5.$6.$7.$8.'|';
            $query =~ s/$_//i;
        } else {
            $content_phones = $content_phones.'7'.$3.'|';
            $query =~ s/$_//i;
        }
    }
    $query =~ s/\+//g;
    $query = trim($query);
    $content_phones =~ s/\|$//g;
    if($query =~/organisation/ && $content_phones ne ''){
        $query =~ s/organisation//g;
        push(
             @{$full_query{body}{query}{bool}{must}},
             {
                "bool" => {
                    "minimum_should_match" => 1,
                    "should" => [
                        { "regexp" => {
                            "owner_phones" => $content_phones
                            }
                        },
                        {
                            "term" => {
                                "mediator_company" => $query
                            }
                        }

                     ],
                }
            }
        );
        $query = '';
    }elsif($content_phones ne ''){
        push(
             @{$full_query{body}{query}{bool}{must}},
             {
                "regexp" => {
                    "owner_phones" => $content_phones
                }
            }
        );
    }

    if(trim($query) ne ''){
        push(
            @{$full_query{body}{query}{bool}{must}},
                { multi_match => {
                            query =>  $query,
                            type => 'cross_fields',
                            operator =>  "and",
                            fields => [ "address", "locality", "mediator_company" ]
                        }
                },
        );
    }

    # if(trim($query) ne ''){
    #     push(
    #         @{$full_query{body}{query}{bool}{must}},
    #             { term => {
    #                         media_info_saller =>  $query
    #                     }
    #             },
    #     );
    # }

    if($change_date ne 'all' && $change_date ne ''){
        my $dt = DateTime->now()->subtract(days => $change_date-1);
        $dt->set(
            hour       => 0,
            minute     => 0,
            second     => 0,
            nanosecond => 0
        );
        push(
            @{$full_query{body}{query}{bool}{must}},
            {
                range => {
                    add_date => {
                        gte => $dt->datetime()
                    }
                }
            }
        );
    }

    if($sort =~/\{addDate=(.+)\}/ ){
        push(
            @{$full_query{body}{sort}},
            {
                add_date => { order => lc($1) }
            }
        );
    }

     say Dumper %full_query;

    my $e = Search::Elasticsearch->new(nodes  => 'import.rplusmgmt.com:9200');
    my $results = $e->search(%full_query);
    return $self->render(json => $results);
}

1;
