#!/bin/bash
ZIPHASH=$(openssl dgst -sha256 $1 | sed 's/.*= //')

jq -n --arg ziphash "$ZIPHASH" '{"ziphash":$ziphash}'