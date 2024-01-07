from bilibili_api import live, sync, Credential

import http.cookies

# 你的 Cookie 文本
cookie_text = "LIVE_BUVID=AUTO2816977204552676; b_nut=1697720455; buvid4=34DB59A6-47D1-B3DC-953E-0E39DB1D2E1655624-023101921-ksPq5hUPXVm6%2BOFFmBjPRg%3D%3D; buvid3=37A48A8B-FF98-401C-B2BE-AC57D04DC1EC27577infoc; _uuid=D10C5239E-95510-3EDF-2A8E-F134F5686EB1069650infoc; buvid_fp_plain=undefined; enable_web_push=DISABLE; header_theme_version=CLOSE; CURRENT_FNVAL=4048; rpdid=|(kJYkJkJ)m|0J'uYm~~mJuYR; DedeUserID=382957163; DedeUserID__ckMd5=537234e3cc45dfda; hit-dyn-v2=1; CURRENT_QUALITY=80; bp_article_offset_382957163=874973829923864664; fingerprint=dff334dfe228c7ed3101952831bcec25; buvid_fp=dff334dfe228c7ed3101952831bcec25; home_feed_column=5; PVID=1; SESSDATA=ebbe501f%2C1720139869%2Ce6249%2A12CjCJU4P7mak9oluUq8CXdXfVZFz-ZPeAica88Ng6LC8xjvHy2BB3Z4m0uXcc_GMY-8ISVncwQndJd3liN3l1dFFVSEo1YndtNGNKUmlfZVN0WEJOOGdyYWQ5LTh6cVotb1ItZGVfWExiV1NVcWdlU3dFczMyRWRhZkF2QV9vQ2pFRzVFeXdvX3dBIIEC; bili_jct=fa9c0262144f89b0bc299c5769defb89; b_lsid=585F22B2_18CE16AA261; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDQ4NTA3NjgsImlhdCI6MTcwNDU5MTUwOCwicGx0IjotMX0.csRZa7_FgulmbJFlkc1OWUPpEvQc7rHu79w2mEv0JNo; bili_ticket_expires=1704850708; sid=6gnena0l; bp_video_offset_382957163=883705876426260483; browser_resolution=1440-779; innersign=0"

# 创建一个 Cookie 对象
cookie = http.cookies.SimpleCookie()
cookie.load(cookie_text)

# 获取 sessdata 和 bili_jct 属性的值
sessdata = cookie.get("SESSDATA")
bili_jct = cookie.get("bili_jct")
# dedeuserid = cookie.get("dedeuserid")
# ac_time_value = cookie.get("ac_time_value")

sessdata_value = sessdata.value
bili_jct_value = bili_jct.value
# dedeuserid_value = dedeuserid.value
# ac_time_value = ac_time_value.value

print(f"sessdata: {sessdata_value}")
print(f"bili_jct: {bili_jct_value}")
# print(f"ac_time_value: {ac_time_value}")

credential = Credential(sessdata=sessdata_value, bili_jct=bili_jct_value,buvid3="")
room = live.LiveDanmaku(room_display_id="27892212", credential=credential)


@room.on('DANMU_MSG')
async def on_danmaku(event):
    # 收到弹幕
    print(event)


@room.on('SEND_GIFT')
async def on_gift(event):
    # 收到礼物
    print(event)


sync(room.connect())
