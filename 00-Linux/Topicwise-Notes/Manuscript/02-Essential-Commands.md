🏗️ Architecture / Deep Dive: Master Command Toolkit
"Chalo, is office building mein ghoomne aur manage karne ke liye apne tools nikalte hain. Main aapko categories mein saare pro-commands dene wala hoon, screen par dhyan rakhna!"

📍 1. Navigation & Discovery (Building mein ghoomna)
"Aap abhi kis floor par ho, ye janne ke liye we have:"

pwd - Print Working Directory (Mera current GPS location).

ls - Room mein kya rakha hai? Iske bohot pro variations hain:

ls -l (Long detail - size, date, permissions)

ls -la (Hidden files bhi dikhayega)

ls -lh (Human readable size, like MBs and GBs)

ls -lt (Time ke hisaab se sort karega)

ls -R (Har folder ke andar tak jhaankega)

ls -ld /etc (Sirf folder ki info dega, uske andar ki nahi)

cd - Change Directory (Ek room se doosre room jana):

cd /path/ (Direct path pe jana), cd ~ (Apne home ghar wapas), cd .. (Ek floor upar), cd - (Pichle wale room mein wapas!), cd / (Main gate/root par).

🆘 2. Getting Help & System Info (Health Check)
"Kabhi phas jao toh building ki help desk hamesha ready hai:"

Help Desk: man ls (Manual padhna), man -k (Keyword se search karna), info ls, whatis ls, which ls, aur whereis ls (Command ki actual location dhundna).

System Check: uname -a (OS details), cat /etc/os-release, hostnamectl.

Hardware Check: lscpu (Processor), lsmem (RAM), lsblk (Hard Disks), lspci, lsusb, dmidecode, aur hwinfo --short.

Uptime & Users: uptime (Server kab se jag raha hai), w (Kaun kaun logged in hai), last, lastlog.

Time Management: date, timedatectl list-timezones (Timezone check karna), aur cal 2025 (Poore saal ka calendar).

History & Clear: clear (ya Ctrl+L), history. Pro tip: !50 likhoge toh history ki 50th command chal jayegi, aur !! last command ko fir se chala dega. Ctrl+R se aap purani commands search kar sakte ho!

🔐 3. File Permissions (VIP Access & ID Cards)
"Linux mein har file ke bahar ek virtual security guard khada hota hai. Access 3 logon ko milta hai: Owner (u), Group (g), aur Others (o)."
Permissions ki value yaad karlo: Read (r) = 4, Write (w) = 2, Execute (x) = 1.

rwx = 4+2+1 = 7 (Full Access)

rw- = 4+2 = 6 (Read+Write)

Common combos: 755 (Scripts ke liye), 644 (Normal files), 600 (Private keys), 777 (Sabke liye open - ⚠️ Avoid!).

Changing Permissions & Owners:

chmod 755 script.sh (Numeric) ya chmod u+x,g-w file.txt (Symbolic - owner ko execute do, group se write chheen lo).

chown alice:developers file.txt (Owner aur Group dono change karna). chgrp sirf group change karta hai.

Special Permissions (Advanced Magic!):

SUID (chmod u+s ya 4755): File run karte time aap wahi power use karoge jo uske owner ki hai.

SGID (chmod g+s ya 2755): Directory ke andar nayi files automatically folder ka group inherit karengi.

Sticky Bit (chmod +t ya 1777): Sirf owner hi apni file delete kar sakta hai (Common in /tmp).

Umask & ACL: umask 0022 decide karta hai nayi files ko default permission kya milegi. Aur agar aur deep control chahiye toh Access Control List use karo: setfacl -m u:bob:rw file.txt (Sirf Bob ko access dena!).

📁 4. File Management (Filing Cabinets)
"Ab files ke sath khelenge, rapidly:"

Create: touch file.txt, echo "Hello" > file.txt (Overwrite), >> (Append). Editors like nano aur vim. Folders ke liye mkdir -p /opt/app/logs (Ek sath saari parent directories bana dega).

Copy/Move: cp -r (Folder copy), cp -p (Permission bacha ke copy), cp -i (Overwrite se pehle poochega). mv (Move ya Rename karna).

Delete (DANGER): rm file.txt, rm -r (Folder delete). ⚠️ NEVER RUN rm -rf / - Ye building mein bomb lagane jaisa hai, sab khatam ho jayega!

View Data: cat -n (Line numbers), less, head -n 20, tail -f /var/log/app.log (Live real-time logs dekhna!), diff -u (2 files mein kya alag hai).

Find (CID Mode): find / -name "*.txt", ya find /tmp -type f -size +100M (100MB se badi files dhundna). Database wali fast search ke liye locate use karo (but updatedb chalana mat bhulna).

Zip & Tar (Suitcase packing):

Compressions: gzip, zip, xz (Best compression), bzip2.

The Boss - tar: tar -cvzf archive.tar.gz files/ (Create Gzip tar) aur nikalne ke liye tar -xvzf archive.tar.gz.

Links (Shortcuts): Hard link (ln file.txt link.txt) same data point karta hai. Symbolic/Soft link (ln -s /path/to/file ~/shortcut) Windows ke shortcut jaisa hota hai! ls -li karke inke inode numbers check kar sakte ho.

💻 Practical / Terminal Touch
"Bohot theoretical power jama kar li, ab thoda hands-on karte hain! Apne terminal par ye chala ke dekho:"

Bash
# 1. Ek log file dhundo jo 7 din se purani ho
find /var/log -name "*.log" -mtime -7

# 2. Us file ko copy karo apni present directory mein
cp /var/log/syslog .

# 3. Last ki 20 lines dekho
tail -n 20 syslog
🗣️ Chat mein answer likho! Agar mujhe ek hi baar mein dir1, uske andar dir2, aur uske andar dir3 banani hai bina error ke... toh mkdir ke aage kaunsa flag (-?) lagana padega? Type in the chat!

🎯 Summary & Outro
"Aaj humne Navigation (cd, ls), Hardware info, File Permissions ki VIP list (chmod, chown, Sticky bits, ACLs), aur Advanced File management (find, tar, symlinks) sab kuch systematically cover kar liya hai!

Quick Recap Question: Agar kisi folder pe 777 permission hai, toh wo system ke liye danger kyun hai? Iska jawab comments mein zarur explain karna!

Linux isn't just an operating system; it's the invisible force running the modern internet, and now, you have the keys to drive it.

Agar script mein maza aaya aur ye heavy data easily samajh aaya, toh hit that Like button, subscribe to the channel, and practice these commands. See you in the next one, keep hacking!"
