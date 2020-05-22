declare DIR="$(cd "$(dirname "$0")/.." && pwd -P)"
mkdir -p "$DIR/build"

if [[ "$1" =~ ^-?a$ ]]; then
  # for uploading to AnkiWeb
  declare addon_id='957961234'
else
  # for installing myself
  declare addon_id='straight_reward'
fi

zip -r "${DIR}/build/${addon_id}.ankiaddon" \
  "${DIR}/config."{json,md} \
  "${DIR}/manifest.json" \
  "${DIR}/user_files/README.md" \
  "${DIR}/__init__.py" \
  "${DIR}/src/"*".py" \
  "${DIR}/src/lib/"*".py" \
  "${DIR}/src/gui/"*".py" \
