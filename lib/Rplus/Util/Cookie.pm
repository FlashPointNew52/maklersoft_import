package Rplus::Util::Cookie;

use utf8;
use Exporter qw(import);

use Cwd qw/abs_path/;
use Mojo::Asset::File;
use Data::Dumper;

our @EXPORT_OK = qw(get_cookie save_cookie);

sub get_coocky {
    my $module = __PACKAGE__;
    my $media = shift;
    my $ip = shift;
    $module =~s/::/\//g;
    my $path = $INC{$module . '.pm'};
    $path =~ s{^(.*/)[^/]*$}{$1};
    $path = abs_path($path . '/../../../cookie/' . $media . '/' .$ip);

    my $file = Mojo::Asset::File->new(path => $path);
    my $config = eval $file->slurp;
    unlink $path;
    return $config;
}

sub save_cookie {
    my $module = __PACKAGE__;
    my $media = shift;
    my $ip = shift;
    my $cookie = shift;
    $module =~s/::/\//g;
    my $path = $INC{$module . '.pm'};
    $path =~ s{^(.*/)[^/]*$}{$1};
    $path = abs_path($path . '../../../cookie/' . $media . '/' .$ip.'.cookie');
    my $file = Mojo::Asset::File->new(path => $path);
    unlink $path;
    $file->cleanup(0);
    $file->add_chunk(join(q{,}, map{qq{\n$_ => $cookie->{$_}}} keys %$cookie));
    $file->slurp;
}

1;
