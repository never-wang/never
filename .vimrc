" do it in this file (/etc/vim/vimrc), since debian.vim will be overwritten
" everytime an upgrade of the vim packages is performed.  It is recommended to
" make changes after sourcing debian.vim since it alters the value of the
" 'compatible' option.

" This line should not be removed as it ensures that various options are
" properly set to work with the Vim-related packages available in Debian.
runtime! debian.vim

set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'gmarik/Vundle.vim'

" The following are examples of different formats supported.
" Keep Plugin commands between vundle#begin/end.
" plugin on GitHub repo
Plugin 'Valloric/YouCompleteMe'
" plugin from http://vim-scripts.org/vim/scripts.html
" Plugin 'L9'
" Git plugin not hosted on GitHub
" Plugin 'git://git.wincent.com/command-t.git'
" git repos on your local machine (i.e. when working on your own plugin)
" Plugin 'file:///home/gmarik/path/to/plugin'
" The sparkup vim script is in a subdirectory of this repo called vim.
" Pass the path to set the runtimepath properly.
" Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
" Avoid a name conflict with L9
" Plugin 'user/L9', {'name': 'newL9'}

" All of your Plugins must be added before the following line
call vundle#end()            " required
" To ignore plugin indent changes, instead use:
"filetype plugin on
"
" Brief help
" :PluginList          - list configured plugins
" :PluginInstall(!)    - install (update) plugins
" :PluginSearch(!) foo - search (or refresh cache first) for foo
" :PluginClean(!)      - confirm (or auto-approve) removal of unused plugins
"
" see :h vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line

" Uncomment the next line to make Vim more Vi-compatible
" NOTE: debian.vim sets 'nocompatible'.  Setting 'compatible' changes numerous
" options, so any other options should be set AFTER setting 'compatible'.
"set compatible

" If using a dark background within the editing area and syntax highlighting
" turn on this option as well
"set background=back

" Uncomment the following to have Vim jump to the last position when
" reopening a file
"if has("autocmd")
"  au BufReadPost * if line("'\"") > 0 && line("'\"") <= line("$")
"    \| exe "normal g'\"" | endif
"endif

" Uncomment the following to have Vim load indentation rules according to the
" detected filetype. Per default Debian Vim only load filetype specific
" plugins.
" if has("autocmd")
"   filetype indent on
" endif

" The following are commented out as they cause vim to behave a lot
" differently from regular Vi. They are highly recommended though.
"set showcmd		" Show (partial) command in status line.
"set showmatch		" Show matching brackets.
"set ignorecase		" Do case insensitive matching
"set smartcase		" Do smart case matching
"set incsearch		" Incremental search
"set autowrite		" Automatically save before commands like :next and :make
"set hidden             " Hide buffers when they are abandoned
"set mouse=a		" Enable mouse usage (all modes) in terminals

"安装了javacomplete和taglist两个插件，都可用在vim.sf.net上下载

"set DoxygenToolkit
let g:DoxygenToolkit_compactOneLineDoc="yes"
"let g:DoxygenToolkit_commentType="C++"
let g:DoxygenToolkit_briefTag_pre="@brief"
"let g:DoxygenToolkit_briefTag_funcName="yes"
let g:DoxygenToolkit_briefTag_post=": "
let g:DoxygenToolkit_paramTag_pre="@param "
let g:DoxygenToolkit_paramTag_post=": "
let g:DoxygenToolkit_returnTag="@return: " 

map <F2> :Dox<CR>

"设置abbreviate
abbreviate #i #include
abbreviate #d #define

"Set mapleader
let mapleader = ","
let g:mapleader = ","

"显示行号
set nu

"打开语法高亮
syntax on

set softtabstop=4
set shiftwidth=4

"关闭自动备份
set nobackup

"自动缩进设置
"set cindent
"set smartindent
"set incsearch
set autoindent

set tabstop=4
set expandtab

"Show matching bracets
set showmatch

"Get out of VI's compatible mode
set nocompatible

"Have the mouse enabled all the time
set mouse=a

"Set to auto read when a file is changed from the outside
set autoread

"Enable filetype plugin
filetype plugin on
filetype indent on
filetype plugin indent on

"设置配色方案为torte
colo torte

"设置支持的文件编码类项，目前设置为utf-8和gbk两种类型
set fileencodings=utf-8,chinese

"设置搜索结果高亮显示
set hlsearch

"Fortran set
let s:extfname=expand("%:e")
if s:extfname==?"f90"
    let fortran_free_source=1
    unlet! fortran_fixed_source
else
    let fortran_fixed_source=1
    unlet! fortran_free_source
endif
let fortran_more_precise=1
let fortran_do_enddo=1
let fortran_have_tabs=1

"设置记录的历史操作列表
set history=50

"设置折叠
"set foldcolumn=2
"set foldmethod=indent
"set foldlevel=3

set modifiable
set write

"AutoCommand
"新建.sh文件，自动插入文件头
autocmd BufNewFile *.sh exec ":call SetTitleShell()"
"新建.py文件，自动插入文件头
autocmd BufNewFile *.py exec ":call SetTitlePython()"
"新建文件后，自动定位到文件末尾
autocmd BufNewFile * normal G

"设置Java代码的自动补全
"au FileType java setlocal omnifunc=javacomplete#Complete

"绑定自动补全的快捷键<C-X><C-O>到<leader>;
imap <leader>; <C-X><C-O>

"设定开关Taglist插件的快捷键为F4，可以在VIM的左侧栏列出函数列表等
map <F4> :Tlist<CR>

"设置程序的运行和调试的快捷键F5和Ctrl-F5
map <F5> :call CompileRun()<CR>
map <C-F5> :call Debug()<CR>


"设置tab操作的快捷键，绑定:tabnew到<leader>t，绑定:tabn, :tabp到<leader>n,
"<leader>p
map <leader>t :tabnew<CR>
map <leader>n :tabn<CR>
map <leader>p :tabp<CR>

" Switch window mappings 
"nmap <C-k> :wincmd k<CR>
"nmap <C-j> :wincmd j<CR>
"nmap <C-l> :wincmd l<CR>
"nmap <C-h> :wincmd h<CR>

"设置下拉菜单的颜色
highlight Pmenu ctermbg=white ctermfg=black
highlight PmenuSel ctermbg=darkblue ctermfg=white

"用cscope支持
set csprg=/usr/bin/cscope
let Tlist_Ctags_Cmd='/usr/bin/ctags'
let Tlist_Show_One_File=1
let Tlist_Exit_OnlyWindow=1
let Tlist_Use_Right_Window=1
"默认打开Taglist
let Tlist_Auto_Open=1

"使用<leader>e打开当前文件同目录中的文件
if has("unix")
    map ,e :e <C-R>=expand("%:p:h") . "/" <CR>
else
    map ,e :e <C-R>=expand("%:p:h") . "\" <CR>
endif

"定义CompileRun函数，用来调用进行编译和运行
func CompileRun()
    exec "w"
    "C程序
    if &filetype == 'c'
        exec "!gcc % -g -o %<"
        exec "!./%<"
        "Java程序
    elseif &filetype == 'java'
        exec "!javac %"
        exec "!java %<"
    endif
endfunc
"结束定义CompileRun


"中文输入支持
:let g:vimim_cloud='sogou'

"定义Debug函数，用来调试程序
func Debug()
    exec "w"
    "C程序
    if &filetype == 'c'
        exec "!gcc % -g -o %<"
        "exec "!gdb %<"
        exec "!insight %<"
        "Java程序
    elseif &filetype == 'java'
        exec "!javac %"
        exec "!jdb %<"
    endif
endfunc
"结束定义Debug

"定义函数SetTitleShell，自动插入文件头
func SetTitleShell()
    call setline(1, "\#!/bin/bash")
    call append(line("."), "\#########################################################################")
    call append(line(".")+1, "\# Author: Wang Wencan")
    call append(line(".")+2, "\# Created Time: ".strftime("%c"))
    call append(line(".")+3, "\# Description: ")
    call append(line(".")+4, "\#########################################################################")
    call append(line(".")+5, "")
endfunc

"定义函数SetTitlePython，自动插入文件头
func SetTitlePython()
    call setline(1, "\#!/usr/bin/env python")
    call append(line("."), "\#########################################################################")
    call append(line(".")+1, "\# Author: Wang Wencan")
    call append(line(".")+2, "\# Created Time: ".strftime("%c"))
    "call append(line(".")+3, "\# File Name: ".expand("%"))
    call append(line(".")+3, "\# Description: ")
    call append(line(".")+4, "\#########################################################################")
    call append(line(".")+5, "")
endfunc

" Source a global configuration file if available
" XXX Deprecated, please move your changes here in /etc/vim/vimrc
if filereadable("/etc/vim/vimrc.local")
    source /etc/vim/vimrc.local
endif

" rename the tmux window with the filename opened in vim
"autocmd BufReadPost,FileReadPost,BufNewFile * call system("tmux rename-window %")

" Protobuf support
augroup filetype
au! BufRead,BufNewFile *.proto setfiletype proto
augroup end

set backspace=indent,eol,start


" YouCompleteMe 设置
let g:ycm_confirm_extra_conf = 0
map <C-W>y :YcmDiag<CR>
"let g:ycm_autoclose_preview_window_after_completion = 1
"let g:ycm_autoclose_preview_window_after_insertion = 1
set completeopt-=preview
let g:ycm_add_preview_to_completeopt = 0
let g:ycm_open_loclist_on_ycm_diags = 1
"set conceallevel=2
"set concealcursor=vin
"let g:clang_snippets=1
"let g:clang_conceal_snippets=1
"" The single one that works with clang_complete
"let g:clang_snippets_engine='clang_complete'
"
"" Complete options (disable preview scratch window, longest removed to aways
"" show menu)
"set completeopt=menu,menuone
"
"" Limit popup menu height
"set pumheight=20
"
"" SuperTab completion fall-back 
"let g:SuperTabDefaultCompletionType='<c-x><c-u><c-p>'


"C-support
"" let g:C_Styles = { '*.c,*.h' : 'default', '*.cc,*.cpp,*.hh' : 'CPP' }

" for gdb
" set previewheight=12
run macros/gdb_mappings.vim
" set asm=0
" set gdbprg=gdb_invocation
