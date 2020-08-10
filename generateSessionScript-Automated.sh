#!/bin/bash

#    Session String Generator for Nana-Remix
#    Copyright (C) 2020 The Pins Team

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

##################################################
# This script was adopted from the Friendly      #
# Telegram auto-installation script. Credits to  #
# the auto-installation script authors.          #
# Link to original code: https://kutt.it/ftgi    #
##################################################


# Check if it's Bash.
if [ ! -n "$BASH" ]; then
  echo "warn:    You're not using Bash, firing up a new Bash console..."
  bash -c '. <('"$(command -v curl >/dev/null && echo 'curl -Ls' || echo 'wget -qO-')"' https://gist.github.com/AndreiJirohHaliliDev2006/7520ca33819abd28eb2b1f9832a9b669/raw/643ce8a5183abe8beb4dcaf9f78b1ffcff6494cb/generate-session-NanaRemix.sh) '"$*"
  exit $?
fi

# Modified version of https://stackoverflow.com/a/3330834/5509575
sp='/-\|'
spin() {
  printf '\b%.1s' "$sp"
  sp=${sp#?}${sp%???}
}
endspin() {
  printf '\r%s\n' "$@"
}

runin() {
  # Runs the arguments and spins once per line of stdout (tee'd to logfile), also piping stderr to logfile
  { "$@" 2>>../ftg-install.log || return $?; } | while read -r line; do
    spin
    printf "%s\n" "$line" >> ../NanaRemix-strsessiongen.log
  done
}

runout() {
  # Runs the arguments and spins once per line of stdout (tee'd to logfile), also piping stderr to logfile
  { "$@" 2>>ftg-install.log || return $?; } | while read -r line; do
    spin
    printf "%s\n" "$line" >> NanaRemix-strsessiongen.log
  done
}

errorin() {
  endspin "$@"
  cat ../NanaRemix-strsessiongen.log
}
errorout() {
  endspin "$@"
  cat NanaRemix-strsessiongen.log
}

pyfiglet -f smslant -w 50 Nana-Remix | sed 's/\\/\\\\/g' | sed 's/"/\\"/g' | sed 's/`/\\`/g' | sed 's/^/printf "%s\\n" "/m;s/$/"/m'
banner() {
  clear
  clear
  printf "%s\n" "   _  __                   ___            _     "
  printf "%s\n" "  / |/ /__ ____  ___ _____/ _ \\___ __ _  (_)_ __"
  printf "%s\n" " /    / _ \`/ _ \\/ _ \`/___/ , _/ -_)  ' \\/ /\\ \\ /"
  printf "%s\n" "/_/|_/\\_,_/_//_/\\_,_/   /_/|_|\\__/_/_/_/_//_\\_\\ "
  printf "%s\n" "                                                "
  printf "%s\n" ""
}

##############################################################################

banner
printf '%s\n' "The bootstrap process will take some time before the session string generation prompt shows up."
printf '%s' "Installing dependencies..."

##############################################################################

echo "Installing dependencies..." > NanaRemix-strsessiongen.log

spin

touch ftg-install.log
if [ ! x"$SUDO_USER" = x"" ]; then
  chown "$SUDO_USER:" NanaRemix-strsessiongen.log
fi

if echo "$OSTYPE" | grep -qE '^linux-gnu.*' && [ -f '/etc/debian_version' ]; then
  PKGMGR="apt-get install -y"
  if [ ! "$(whoami)" = "root" ]; then
    # Relaunch as root, preserving arguments
    if command -v sudo >/dev/null; then
      endspin "Restarting as root..."
      echo "Relaunching" >>ftg-install.log
      sudo "$BASH" -c '. <('"$(command -v curl >/dev/null && echo 'curl -Ls' || echo 'wget -qO-')"' https://gitlab.com/friendly-telegram/friendly-telegram/-/raw/master/install.sh) '"$*"
      exit $?
    else
      PKGMGR="true"
    fi
  else
    runout dpkg --configure -a
    runout apt-get update  # Not essential
  fi
  PYVER="3"
elif echo "$OSTYPE" | grep -qE '^linux-gnu.*' && [ -f '/etc/arch-release' ]; then
  PKGMGR="pacman -Sy --noconfirm"
  if [ ! "$(whoami)" = "root" ]; then
    # Relaunch as root, preserving arguments
    if command -v sudo >/dev/null; then
      endspin "Restarting as root..."
      echo "Relaunching" >>ftg-install.log
      sudo "$BASH" -c '. <('"$(command -v curl >/dev/null && echo 'curl -Ls' || echo 'wget -qO-')"' https://gitlab.com/friendly-telegram/friendly-telegram/-/raw/master/install.sh) '"$*"
      exit $?
    else
      PKGMGR="true"
    fi
  fi
  PYVER="3"
elif echo "$OSTYPE" | grep -qE '^linux-android.*'; then
  runout apt-get update
  PKGMGR="apt-get install -y"
  PYVER=""
elif echo "$OSTYPE" | grep -qE '^darwin.*'; then
  if ! command -v brew >/dev/null; then
    ruby <(curl -fsSk https://raw.github.com/mxcl/homebrew/go)
  fi
  PKGMGR="brew install"
  PYVER="3"
else
  endspin "Unrecognised OS. Please manually clone the repository (https://github.com/pokurt/Nana-Remix) and run the 'strNana.py' file."
  exit 1
fi
