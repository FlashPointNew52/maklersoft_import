#!/usr/bin/env perl

use FindBin;
use lib "$FindBin::Bin/../lib";

use Minion;

use Mojo::IOLoop;
use Rplus::Modern;
use Rplus::Class::Media;

use Rplus::Import::QueueDispatcher;
use Rplus::Import::ItemDispatcher;
use Rplus::Util::Config qw(get_config);
use URI::Encode qw(uri_encode uri_decode);

use Data::Dumper;

no warnings 'experimental';

my $minion = Minion->new(Pg => 'postgresql://raven:raven!12345@localhost/rplus_import');
my $timer = 1800;
while (my $arg = shift @ARGV){
    if ($arg eq '-t'){
        $timer = shift @ARGV;
    };
}


say '<<<<<<<<<<------------------------------------------------->>>>>>>>>>';
#$minion->reset;
say Dumper $minion->stats;
$minion->backoff(sub {return 300;});

say "Loop timer is $timer sec";
while(1){
    my $load_list = get_config('load_list')->{load_list};
    foreach my $mname (keys %{$load_list}) {
        my $loc_list = $load_list->{$mname};
            foreach my $lname (@$loc_list) {
                my $mc = Rplus::Class::Media->instance();
                my $media_data = $mc->get_media($mname, $lname);

                foreach (@{$media_data->{source_list}}) {
                    my $category = $_->{url};

                    say 'enqueue enq task ' . $mname . ' - ' . $lname . ' - ' . $category;

                    $minion->enqueue(
                        enqueue_task => [
                            {media => $mname, location => $lname, category => $category}
                        ], {
                            attempts => 3,
                            priority => 10,
                            queue => $mname,
                        }
                    );

                }
            }
    }
    sleep($timer);
}
