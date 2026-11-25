#!/bin/bash
cd /mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro || exit 1
rm -rf out_ext && mkdir -p out_ext
cands=(
 "SweetBlood" "Sweetblood" "sweetblood" "SWEETBLOOD"
 "SweetBl00d" "SweetBL00D" "SweetBL000d" "SweetBL00D" "SweetBl0od" "SweetB100d"
 "SweetBlood1810" "SweetBL00d1810" "SweetBl00d1810"
 "KEY: SweetBlood" "KEY:SweetBlood" "key: sweetblood" "KEY: SweetBl00d"
 "SweetBlood2024" "SweetBlood2025" "SweetBlood2026"
 "ElSusurro" "susurro" "Susurro" "SUSURRO"
 "DRACULA" "dracula" "Conde" "conde"
)
for p in "${cands[@]}"; do
  r=$(steghide extract -sf ChismeAudio.wav -p "$p" -xf "out_ext/$p.bin" 2>&1)
  if echo "$r" | grep -q "extracted"; then
    echo ">>> EXITO con: [$p]  -> $r"
  else
    echo "no: [$p]"
  fi
done
ls -l out_ext
