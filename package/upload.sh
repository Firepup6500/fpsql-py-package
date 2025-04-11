source .env
if [ -z ${PYPI_TOKEN+x} ]; then
	echo 'Cannot upload without a pypi token. Please set one in a .env file next to this script with the name of `PYPI_TOKEN`.'
	exit 1
fi
echo "🧽 Pruging old package files... 🧽"
rm -rf dist
mkdir dist
echo "🧹 Formatting... 🧹"
black . > /dev/null
echo "🛠  Building... 🛠"
poetry build > /dev/null
echo -n "☁️  Uploading... ☁️"
poetry publish -u __token__ -p $PYPI_TOKEN
echo "✨ All done! ✨"
unset PYPI_TOKEN
