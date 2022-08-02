# Python-get-hatena-info


## 概要 Description
はてなブログの各記事に付いたスターとブックマークの数を取得して CSV ファイルに出力するアプリ   

はてなブログの各APIを使用して記事に付いたスターとブックマークの数を取得し、CSVファイルに出力します。  
Use each API of Hatena Blog to get the number of stars and bookmarks attached to the article and output it to a CSV file.  

## 特徴 Features

- はてなブログのURLを指定して各記事のスターの数とブックマークの数を出力  
	Output the number of stars and bookmarks of each article by specifying the URL of the Hatena blog  
- スターの数は色ごとに出力  
	The number of stars is output for each color  
- 結果は CSV ファイルに出力  
	Results output to CSV file  
	- CSV ファイルの出力項目  
		CSV file output items  
		url,title,published,updated,bookmark,yellow,green,red,blue,purple  
		,category,eye_catch  
- 出力する記事の数を指定可能  
	You can specify the number of articles to output  

## 依存関係 Requirement

- Python 3.8.5  
- Requests 2.25.1  

## 使い方 Usage

```dosbatch
	get_hatena_info.exe
```

- 操作 Operation  
	- 設定ファイル(settings_hatena_url.py)の編集  
		Edit configuration file(settings_hatena_url.py)  
		- ブログのURL、ページ数を指定  
			Specify the URL of the blog and the number of pages
	- アプリの起動  
		Launch the app  
	- 出力されたCSVファイルの確認  
		Check the output CSV file

## インストール方法 Installation

なし  

## プログラムの説明サイト Program description site

- [はてなブログ、スター、ブックマーク用APIの使い方【Python】 - プログラムでおかえしできるかな](https://juu7g.hatenablog.com/entry/Python/blog/get-stars-bm-prog)  
- [はてなブログのアイキャッチ画像のURLの取り方【Python】 - プログラムでおかえしできるかな](https://juu7g.hatenablog.com//entry/Python/blog/get-eye-catch)

## 作者 Authors
juu7g

## ライセンス License
このソフトウェアは、MITライセンスのもとで公開されています。LICENSE.txtを確認してください。  
This software is released under the MIT License, see LICENSE.txt.

