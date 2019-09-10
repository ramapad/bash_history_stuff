Scripts to keep track of bash history in *nix forever and recover from crashes of .bash_history

---------------------------------------------------------------------------

I like to keep track of the commands I executed in bash forever. This involves two things:
(i) Updating .profile/.bashrc to request history storage forever
(ii) Taking steps to ensure that we can restory history even if a crash occurs

---------------------------------------------------------------------------

(i) Update .profile/.bashrc to store history forever:

# In order to store commands from all different instances of the terminal in the history file. Or also known as - to keep command history from multiple bash sessions.
shopt -s histappend

# To ask for a heck of a lot of history to be stored. 
export HISTSIZE=100000
export HISTFILESIZE=1000000

---------------------------------------------------------------------------


(ii) Taking steps to ensure that we can restory history even if a crash occurs

(a) Create a cron job to backup history periodically
- I have a simple Python script to copy .bash_history:
python make_history_bkup.py
- Include the following line in crontab:
5 * * * * python /home/ramapad/make_history_bkup.py

(b) A script to restore history after a crash:
- I wrote a script that will use the backups created by the cron jobs to stitch together the history file from all the backups:
python fix_history.py .bash_history_consolidated