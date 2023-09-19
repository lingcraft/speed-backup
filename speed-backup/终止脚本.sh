if [ -f "${0%/*}/tools/bin/tools.sh" ]; then
	MODDIR="${0%/*}"
	[[ $(find "$MODDIR" -maxdepth 1 -name "*.zip" -type f 2>/dev/null) ]] && echo "警告！此脚本不能拿来更新脚本" && exit 2
	. "$MODDIR/tools/bin/tools.sh"
	echoRgb "等待脚本停止中，请稍后....."
	kill_Serve && echoRgb "脚本终止"
	exit
else
	echo "$MODDIR/tools/bin/tools.sh遗失"
fi