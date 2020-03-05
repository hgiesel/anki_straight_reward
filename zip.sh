declare DIR=${BASH_SOURCE%/*}

if [[ "$1" == '-a' ]]; then
  # for uploading to AnkiWeb
  declare addon_id='957961234'
else
  # for installing myself
  declare addon_id='straight_reward'
fi

rm -f "${DIR}/${addon_id}.ankiaddon"

zip -r "${DIR}/${addon_id}.ankiaddon" \
  "${DIR}/config."{json,md} \
  "${DIR}/manifest.json" \
  "${DIR}/user_files/README.md" \
  "${DIR}/__init__.py" \
  "${DIR}/src/"*".py" \
  "${DIR}/src/lib/"*".py" \
  "${DIR}/src/gui/"*".py" \
