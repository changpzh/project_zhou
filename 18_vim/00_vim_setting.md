### put below infor in /etc/vim/vimrc file.

    " change vim tapsapce to 4 spaces"
	set tabstop=4
	set softtabstop=4
	" 你希望一个缩进量代表的空格的数目"
	set shiftwidth=4
	set noexpandtab 
	set expandtab

	" control indent"
	set autoindent
	
	" 行号"
	set nu　　　　　　
	
	"Hightlight cursor line in vim"
	:set cursorline
	:set cursorcolumn

	"change Hight light color and style"
	highlight CursorLine   cterm=NONE ctermbg=black ctermfg=green guibg=NONE guifg=NONE
	highlight CursorColumn cterm=NONE ctermbg=black ctermfg=green guibg=NONE guifg=NONE


###1、vim ~/.vimrc 进入配置文件

	如果不知道vimrc文件在哪，可使用 :scriptnames 来查看

	set nu　　　　　　#行号

	set tabstop=4　　#一个tab为4个空格长度

	set ai  #设置自动缩进

	syntax on   #高亮