#!/bin/bash
# Verifica contraseñas contra /etc/shadow de la guest (hashes yescrypt $y$).
# john/hashcat no soportan yescrypt; crypt() de Perl (libxcrypt) sí.
# Uso: ./crack_yescrypt.sh <shadow> <diccionario>
# Resultado conocido: root -> Tr4bajo_1nt3rn0_2024
set -euo pipefail
SHADOW="${1:-work/shadow_galvarino_root.txt}"
CAND="${2:-work/candidatos_password.txt}"

perl -e '
my ($F,$C)=@ARGV;
open(my $fh,"<",$F) or die "no puedo abrir $F: $!";
my %h;
while(<$fh>){ chomp; my @p=split/:/; $h{$p[0]}=$p[1] if @p>1; }
open(my $c,"<",$C) or die "no puedo abrir $C: $!";
my @cand=<$c>; chomp @cand;
for my $u (sort keys %h){
  my $hh=$h{$u};
  next if !$hh || $hh eq "!" || $hh eq "*";
  my $found="";
  for my $p (@cand){
    my $x = crypt($p,$hh);
    if (defined $x && $x eq $hh){ $found=$p; last; }
  }
  printf "%-10s %s\n", $u, ($found ? "PASSWORD=$found" : "sin coincidencia");
}
' "$SHADOW" "$CAND"
