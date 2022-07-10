"""
はてなブログのデータを取得する
"""

from base64 import b64encode
from hashlib import sha1
from typing import Tuple
import sys, os, secrets, csv
from datetime import datetime
import requests
import xml.etree.ElementTree as ET
sys.path.append(os.path.dirname(sys.executable))    # exeから読めるようにパスに追加
import settings_hatena_url

class HatenaBlogAtom():
    """
    はてなブログへアクセスするためのAtomクラス
    """
    def get_star_num(self, stars) -> int:
        """
        はてなスターのタグから数を集計。countタグがある時はその数、無い時は1
        タグは、name, quote, countのリスト。countはない場合がある
        Args:
            list:   スター情報のリスト
        Returns:
            int:    スターの数
        """
        item_num = len(stars)
        for star_ in stars:
            if "count" in star_:
                item_num = item_num + star_.get("count") - 1
        return item_num

    def get_hatena_stars(self, url:str) -> dict:
        """
        はてなスター情報をリクエストして取得。スターの色ごとに数を値にした辞書を作成
        情報は、uri, starts, colored_starsのリスト。colored_starsはない場合がある
        colored_starsはcolor, starsのリスト。
        Args:
            str:    スターを集計する記事のURL
        Returns:
            dict:   色ごとのスターの数の辞書
        """
        endpoint = f"https://s.hatena.com/entry.json?uri={url}"
        r = requests.get(endpoint)
        stars_num = {"yellow":0, "green":0, "red":0, "blue":0, "purple":0}
        if r.status_code == 200:
            for entry_ in r.json().get("entries"):
                item_num = self.get_star_num(entry_.get("stars"))   # 黄色スターの数を求める
                stars_num["yellow"] += item_num
                if entry_.get("colored_stars"):     # 黄色以外のスターの数を求める
                    for colored_star_ in entry_.get("colored_stars"):
                        n = self.get_star_num(colored_star_.get("stars"))
                        stars_num[colored_star_.get("color")] += n
            # print(f"Star count:{stars_num}")
        return stars_num

    def get_hatena_bookmark(self, url:str) -> int:
        """
        はてなブックマーク情報をリクエストして取得。ブックマークの数を返す
        Args:
            str:    ブックマークを集計する記事のURL
        Returns:
            int:    ブックマークの数
        """
        endpoint = f"https://bookmark.hatenaapis.com/count/entry?url={url}"
        r = requests.get(endpoint)
        j = None
        if r.status_code == 200:
            j = r.json()    # 個数が返る
        # print(f"Bookmark count:{j}")
        return j

    def get_article_info(self, xml:str) -> Tuple[str, dict]:
        """
        コレクション応答XMLから記事の情報を取得
        Args:
            str:    XML文書
        Returns:
            str:    次の記事のurl
            dict:   記事の情報の辞書(キーはURL、値は辞書)
        """
        root = ET.fromstring(xml)

        ns = {'': 'http://www.w3.org/2005/Atom'}    # デフォルト名前空間の指定

        # 次ページ用タグの取得
        # linkタグの属性relがnextのものを検索。無い場合を考慮
        next_el = root.find(".link/[@rel='next']", ns)
        if ET.iselement(next_el):       # エレメント自体を判定するとうまくいかない
            next_ = next_el.get("href") # urlの取得
        else:
            next_ = None

        article_info = {}

        entry_iter = root.iter("{http://www.w3.org/2005/Atom}entry")  # iterは名前空間辞書は使えない
        for entry_ in entry_iter:
            # entryタグの子から記事の属性を取得
            link_ = entry_.find(".link/[@rel='alternate']", ns).get("href") # 記事のURL
            title_ = entry_.find("title", ns).text                          # 記事のタイトル
            updated_ = entry_.find("updated", ns).text                      # 記事の更新日
            updated_ = updated_.replace("+09:00", "")                       # csvをエクセルで開いた時に見やすくするための置換
            updated_ = updated_.replace("T", " ")                           # yy:mm:ddThh:mm:ss+09:00⇒yy:mm:dd hh:mm:ss
            published_ = entry_.find("published", ns).text                  # 記事の投稿日
            published_ = published_.replace("+09:00", "")
            published_ = published_.replace("T", " ")
            category_list = entry_.findall("category", ns)                  # 記事のカテゴリ
            category_ = [element_.get("term") for element_ in category_list]    # カテゴリは複数あるのでまずリストに
            category_ = ",".join(category_)                                     # Notionで扱いやすいようにカンマ区切りの文字列に
            # 取得した情報を辞書に、後でcsv出力しやすいように、キーはURL
            article_info[link_] = {"title":title_, "published":published_
                                , "updated":updated_, "category":category_}
        return  next_, article_info
        
    def wsse(self, username: str, api_key: str) ->str:
        """
        WSSE認証
        Args:
            str:        はてなブログのユーザーID
            str:        はてなブログのapi key
        Returns:
            str:        送信用認証WSSEデータ
        """
        # 安全なnonceの生成
        # token_urlsafe()で生成してBase64でエンコードしたが長さは4の倍数でないとデコードできない
        # "="を付加して長さを調整する方法もあるようだがエンコードできるか心配なのでバイト型で作成してエンコードする
        # nonce64 = secrets.token_urlsafe(16)  
        nonce = secrets.token_bytes()                   # 安全な乱数発生
        nonce64 = b64encode(nonce).decode()             # b64encodeはバイト型のため文字型に変換
        created = datetime.utcnow().isoformat() + "Z"   # UTC(協定世界時)でiso表記

        # PasswordDigest：Nonce, Created, APIキーを文字列連結し、SHA1アルゴリズムでダイジェスト化
        # 更にBase64エンコード
        password_digest = nonce + created.encode() + api_key.encode()    # sha1の入力はバイト型のため
        password_digest = sha1(password_digest).digest()
        password_digest = b64encode(password_digest).decode()

        # WSSE認証文字列作成
        s = f'UsernameToken Username="{username}", PasswordDigest="{password_digest}", Nonce="{nonce64}", Created="{created}"'
        return s

    def get_hatena(self, next_url:str = None) -> str:
        """
        はてなブログの記事取得
        Args:
            str:    None:ブログのトップ画面を取得する場合
                    url:前回の取得で得られた次のページのurl
        Returns:
            str:    xml
        """
        blog_id = settings_hatena_url.blog_id
        headers = {'X-WSSE': self.wsse(os.getenv("py_hatena_username"), os.getenv("py_hatena_api_key"))}
        if next_url:
            endpoint = next_url
        else:
            endpoint = f'https://blog.hatena.ne.jp/{os.getenv("py_hatena_username")}/{blog_id}/atom/entry'    # コレクション
            # endpoint = f'https://blog.hatena.ne.jp/{os.getenv("py_hatena_username")}/{blog_id}/atom'    # サービス文書
        
        try:
            r = requests.get(endpoint, headers=headers)

            print(f'--request result-- status code={r.status_code}')
            r.raise_for_status()    # 200番代以外は例外を発生
            # 例外がないのでxmlを返す
            result = r.text
        except requests.exceptions.ConnectionError:
            sys.stderr.write('Connection Error!')
            result = ""
        except:
            sys.stderr.write(f'Error!\nstatus_code: {r.status_code}\nmessage: {r.text}')
            result = ""
        return result
        
    def output_xml(self, text:str):
        """
        XML出力 ファイルはカレントディレクトリに「hatenaxml_yymmddHHMM.xml」
        Args:
            str:    xml string
        """
        logfile_name = f"hatenaxml_{datetime.now().strftime('%y%m%d%H%M')}.xml"
        msg = f"{text}"
        try:
            with open(logfile_name, mode="w", encoding="utf_8") as file_:
                file_.write(msg)
        except Exception as e:
            print(f"書き込みエラー：{e}")

    def output_results2csv(self, blog_info:list):
        """
        XML出力 ファイルはカレントディレクトリに「hatenablog_sb_yymmddHHMM.xml」
        エンコードはBOM付UTF-8。BOM付だとエクセルで文字化けしない。
        Args:
            str:    xml string
        """
        logfile_name = f"hatenablog_sb_{datetime.now().strftime('%y%m%d%H%M')}.csv"
        try:
            with open(logfile_name, mode="w", encoding="utf_8_sig", newline="") as file_:
                # 辞書から出力するので辞書のキーをヘッダーとして定義する
                csv_fields = ["url", "title", "published", "updated", "bookmark", "yellow", "green", "red", "blue", "purple", "category"]
                csv_writer = csv.DictWriter(file_, fieldnames=csv_fields)
                csv_writer.writeheader()
                csv_writer.writerows(blog_info)
        except Exception as e:
            print(f"書き込みエラー：{e}")

    def get_star_and_bookmark_from_urls(self, blog_dict:dict) -> list:
        """
        はてなスターの数とはてなブックマークの数を取得して付加する
        Args:
            dict:   記事情報の辞書(キーはURL)取得した記事の数だけある
        Returns:
            list:   記事属性(辞書)のリスト
        """
        article_info = []
        for url, value in blog_dict.items():
            stars_dict = self.get_hatena_stars(url)         # はてなスター数の取得(色をキーにした辞書)
            bookmark_num = self.get_hatena_bookmark(url)    # はてなブックマーク数の取得
            stars_dict["url"] = url                         # スターの辞書にURLを追加
            stars_dict["bookmark"] = bookmark_num           # スターの辞書にブックマーク数を追加
            stars_dict.update(value)                        # スターの辞書に記事情報(辞書)を追加
            article_info.append(stars_dict)                 # スターの辞書を記事属性の辞書としてリストに追加
        return article_info

if __name__ == '__main__':
    hatena_atom = HatenaBlogAtom()

    pages = settings_hatena_url.pages   # 取得するトップページのページ数
    page = 1                            # 処理しているページ
    next_blog_url = None
    articles_info = []
    print(f"Start from URl:{settings_hatena_url.blog_id}")

    # pagesが0ならずっと、指定されていればそのページまで処理を繰り返す
    while page <= pages or pages == 0:
        # DEBUG
        debug = False
        if debug:
            # 取得したxmlファイルで動作確認
            path = r'hatenaxml_220524.xml'
            with open(path, mode="r", encoding="utf-8") as f:
                result_xml = f.read()
        else:
            result_xml = hatena_atom.get_hatena(next_blog_url)  # はてなブログへリクエストと結果取得
            # hatena_atom.output_xml(result_xml)                # デバッグ、解析用にxml出力

        if not result_xml:
            print("\nエラー終了：URLが存在しないか、ユーザ ID か API key が誤っています")
            input("\n確認したらEnterキーを押してください")
            sys.exit(1)
        
        # はてなブログのコレクションを解析して記事情報を取得
        next_blog_url, article_info1 = hatena_atom.get_article_info(result_xml)
        print(f"Next URL:{next_blog_url}")

        # はてなスター、ブックマークの数を取得
        page_result_ = hatena_atom.get_star_and_bookmark_from_urls(article_info1)
        articles_info += page_result_  # リストにリストを追加

        # 次ページのURIが無くなったら終了
        if next_blog_url:
            page += 1
        else:
            break

    hatena_atom.output_results2csv(articles_info)
    print("Finished")
    input("\n確認したらEnterキーを押してください")
