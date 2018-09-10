package Rplus::Class::UserAgent {

    use Rplus::Modern;
    use Mojo::UserAgent;
    use Mojo::UserAgent::CookieJar;
    use Data::Dumper;

    sub new {
        my ($class, $interface) = @_;

        say 'using if: ' . $interface;

        my $ua = Mojo::UserAgent->new;
        $ua->max_redirects(4);
        $ua->local_address($interface);
        my $self = {
          name => 'UserAgentWrapper',
          ua => $ua
        };

        bless $self, $class;

        return $self;
    }

    sub get_res {
        my ($self, $url, $headers, $ret_req) = @_;

        my $res;
        my $req;
        my $retry = 3;

        while ($retry > 0) {
            $retry -= 1;

            say $url;

            my $t = $self->{ua}->get($url, {
                @{$headers},
                'Connection' => 'keep-alive',
                'Cache-Control' => 'max-age=0',
                'User-Agent' => 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
                'Accept-Encoding' => 'gzip,deflate,sdch',
                'Accept-Language' => 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
            });
            if ($t->res && $t->res->code) {
                if ($t->res->code == 200) {
                    $res = $t->res;
                    $req = $t->req;
                    #say Dumper $t->req;
                    last;
                } elsif ($t->res->code == 404) {
                    last;
                }
            } else {
                say $url;
                say Dumper $t;
            }
            sleep 3;

        }
        if($ret_req){
            return [$res, $req];
        } else {
            return $res;
        }

    }

    sub get_transaction {
        my ($self, $url, $add_headers, $ret_req, $cookie) = @_;

        my $res;
        my $req;
        my $retry = 3;

        my $t = $self->{ua}->build_tx(GET => $url);
        $t->req->headers->connection('keep-alive');
        $t->req->headers->cache_control('max-age=0');
        $t->req->headers->accept_encoding('gzip,deflate,sdch');
        $t->req->headers->user_agent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36');
        $t->req->headers->accept_language('ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4');
        for my $key ( keys %$add_headers ) {
            my $value = %$add_headers{$key};
            $t->req->headers->header($key => $value);
        }
        foreach (@{$cookie}){
            $t->req->cookies($_);
        }
        say Dumper $t->req->headers;
        #say 'get answwer';
        $t = $self->{ua}->start($t);
        if ($t->res && $t->res->code) {
            if ($t->res->code == 200) {
                $res = $t->res;
                $req = $t->req;
                #say Dumper $t->req;
            } elsif ($t->res->code == 404) {
            }
        } else {
            say $url;
            say Dumper $t;
        }
        say Dumper $t->res->headers;
        if($ret_req){
            return [$res, $req];
        } else {
            return $res;
        }
    }

    sub cookie_jar {
        my ($self) = @_;
        return $self->{ua}->cookie_jar;
    }

}

1;
