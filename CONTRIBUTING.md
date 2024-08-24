
# hatchをつかって管理する

好みの方法でhatchをインストールする
※ OS上に直接インストールできるが、私はpython環境以外を汚したくないのでpipを使った。
```
pip install hatch
```

# テスト

以下を実行し
```
hatch shell tests 
```
テスト用仮想環境に入り
```
hatch test
```
でパッケージに対するテストが実行できます


# ドキュメントを編集するときは

docsブランチを作成
```
git checkout main
git checkout -b docs
git push -u origin docs
```

※`git branch -a`で作成したブランチを確認

# ソースコードからドキュメントを作成
```
hatch shell docs
sphinx-quickstart docs
sphinx-apidoc -f -o ./docs/source ./src/tvtsplit
cd docs
make html
```

