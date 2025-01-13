@app.route('/watch')
def watch():
    """動画情報を取得してテンプレートにレンダリング"""
    videoid = request.args.get('v')  # ?v=videoidの形式でvideoidを取得
    if not videoid:
        return "Error: videoid not provided", 400

    # APIのURLを構築
    url = f"https://www.googleapis.com/youtube/v3/videos?id={videoid}&key={API_KEY}&part=snippet,contentDetails,statistics,status,liveStreamingDetails,player,topicDetails"

    try:
        # APIからJSONを取得
        response = requests.get(url)
        video_info = response.json()

        # レスポンスに動画が含まれていればその情報をテンプレートに渡してレンダリング
        if 'items' in video_info:
            video = video_info['items'][0]

            # ここで関連動画を取得
            tags = video['snippet'].get('tags', [])
            channel_id = video['snippet']['channelId']
            category_id = video['snippet']['categoryId']

            # `search.list` APIを使って関連動画を検索
            search_url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&type=video&part=snippet&q={tags[0]}&maxResults=5"
            related_response = requests.get(search_url)
            related_videos = related_response.json().get('items', [])

            return render_template('video.html', video=video, related_videos=related_videos)
        else:
            return "Error: Video not found", 404

    except Exception as e:
        return str(e), 500
