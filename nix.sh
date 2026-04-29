#!/bin/bash

nix profile remove user-packages
nix profile install --file ./packages.nix
