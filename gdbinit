set auto-load safe-path /
source ~/.cs444/gdb-dashboard.py
set history save
set verbose off
set print pretty on
set print array off
set print array-indexes on
set python print-stack full

python Dashboard.start()

dashboard -layout registers assembly source stack memory expressions

dashboard registers -style list 'rax rbx rcx rdx rsi rdi rbp rsp r8 r9 r10 r11 r12 r13 r14 r15 rip eflags cs ss ds es fs gs'
