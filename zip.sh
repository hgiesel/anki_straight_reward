declare DIR=${BASH_SOURCE%/*}

npm run --prefix "${DIR}/js" build

if [[ "$1" == '-a' ]]; then
  # for uploading to AnkiWeb
  declare addon_id='??'
else
  # for installing myself
  declare addon_id='straight_reward'
fi

rm -f "${DIR}/${addon_id}.ankiaddon"

zip -r "${DIR}/${addon_id}.ankiaddon" \
  "${DIR}/config."{json,md} \
  "${DIR}/manifest.json" \
  "${DIR}/__init__.py" \
  "${DIR}/src/"*".py" \
  "${DIR}/src/lib/"*".py" \
  "${DIR}/src/gui/"*".py" \
