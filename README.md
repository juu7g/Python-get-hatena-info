# Python-get-hatena-info


## �T�v Description
�͂Ăȃu���O�̊e�L���ɕt�����X�^�[�ƃu�b�N�}�[�N�̐����擾���� CSV �t�@�C���ɏo�͂���A�v��   

�͂Ăȃu���O�̊eAPI���g�p���ċL���ɕt�����X�^�[�ƃu�b�N�}�[�N�̐����擾���ACSV�t�@�C���ɏo�͂��܂��B  
Use each API of Hatena Blog to get the number of stars and bookmarks attached to the article and output it to a CSV file.  

## ���� Features

- �͂Ăȃu���O��URL���w�肵�Ċe�L���̃X�^�[�̐��ƃu�b�N�}�[�N�̐����o��  
	Output the number of stars and bookmarks of each article by specifying the URL of the Hatena blog  
- �X�^�[�̐��͐F���Ƃɏo��  
	The number of stars is output for each color  
- ���ʂ� CSV �t�@�C���ɏo��  
	Results output to CSV file  
	- CSV �t�@�C���̏o�͍���  
		CSV file output items  
		url,title,published,updated,bookmark,yellow,green,red,blue,purple  
		,category,eye_catch  
- �o�͂���L���̐����w��\  
	You can specify the number of articles to output  

## �ˑ��֌W Requirement

- Python 3.8.5  
- Requests 2.25.1  

## �g���� Usage

```dosbatch
	get_hatena_info.exe
```

- ���� Operation  
	- �ݒ�t�@�C��(settings_hatena_url.py)�̕ҏW  
		Edit configuration file(settings_hatena_url.py)  
		- �u���O��URL�A�y�[�W�����w��  
			Specify the URL of the blog and the number of pages
	- �A�v���̋N��  
		Launch the app  
	- �o�͂��ꂽCSV�t�@�C���̊m�F  
		Check the output CSV file

## �C���X�g�[�����@ Installation

�Ȃ�  

## �v���O�����̐����T�C�g Program description site

- [�͂Ăȃu���O�A�X�^�[�A�u�b�N�}�[�N�pAPI�̎g�����yPython�z - �v���O�����ł��������ł��邩��](https://juu7g.hatenablog.com/entry/Python/blog/get-stars-bm-prog)  
- [�͂Ăȃu���O�̃A�C�L���b�`�摜��URL�̎����yPython�z - �v���O�����ł��������ł��邩��](https://juu7g.hatenablog.com//entry/Python/blog/get-eye-catch)

## ��� Authors
juu7g

## ���C�Z���X License
���̃\�t�g�E�F�A�́AMIT���C�Z���X�̂��ƂŌ��J����Ă��܂��BLICENSE.txt���m�F���Ă��������B  
This software is released under the MIT License, see LICENSE.txt.

