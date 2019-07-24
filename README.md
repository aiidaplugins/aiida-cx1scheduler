# aiida_icl

AiiDA plugin for working with HPC at Imperial College London.

Provides the `aiida.scheduler` entry point: `pbspro_cx1`.

To create a new Computer:

```python
from aiida import load_profile()
from aiida_icl.utils import get_cx1_computer
load_profile()
computer = get_cx1_computer('/path/to/workdir', '/Users/user_name/.ssh/id_rsa')
print(computer)
```

```text
icl_cx1 (login.cx1.hpc.ic.ac.uk), pk: 8
```

To generate calculation `metadata.options`:

```python
from aiida_icl.utils import JOB_CLASSES, get_calulation_options
options = get_calulation_options(JOB_CLASSES.general_24)
print(options)
```

```python
{'resources': {'num_machines': 1, 'num_mpiprocs_per_machine': 32}, 'max_memory_kb': 10000000, 'max_wallclock_seconds': 86400, 'withmpi': True}
```

## Setting up an SSH Public and Private Keys

Rather than directly using a password to access the remote host, public key authentication is used, as a more secure authentication method. There are numerous explanations on the internet
(including [here](https://help.ubuntu.com/community/SSH/OpenSSH/Keys)) and below follows a short setup guide
(taken from [here](https://wiki.ch.ic.ac.uk/wiki/index.php?title=Mod:Hunt_Research_Group/SSHkeyfile)):

First open a shell on the computer you want to connect from. Enter cd ~/.ssh.
If an `ls` shows to files called 'id_rsa' and 'id_rsa.pub' you already have a key pair.
If not, enter `ssh-keygen` Here is what the result should look like:

```console
heiko@clove:~/.ssh$ ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/Users/heiko/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in id_rsa.
Your public key has been saved in id_rsa.pub.
The key fingerprint is:
f0:da:dc:77:cf:71:12:c8:50:dc:18:a9:8d:66:38:ae heiko@clove.ch.ic.ac.uk
The key's randomart image is:
+--[ RSA 2048]----+
|           .o=   |
|           .+ .  |
|      .  ..+     |
|       oo =o..   |
|       .S+  o .  |
|       +..     . |
|      ..o . . o..|
|      E    . . +o|
|                o|
+-----------------+
```

You should keep the standard directory and choose a suitably difficult passphrase.

The two file you just created are key and keyhole. The first file 'id_rsa' is the key.
You should not ever ever ever give it to anybody else or allow anyone to copy it.
The second file 'id_rsa.pub' the keyhole. It is public and you could give it to anyone.
In this case, give it to the hpc.

If you open 'id_rsa.pub' it should contain one line of, similar to:

```console
ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAwRDgM+iQg7OaX/CFq1sZ9jl206nYIhW9SMBqsOIRvGM68/6o6uxZo/D4IlmQI9sAcU5FVNEt9dvDanRqUlC7ZtcOGOCqZsj1HTGD3LcOiPNHYPvi1auEwrXv1hDh4pmJwdgZCRnpewNl+I6RNBiZUyzLzp0/2eIyf4TqG1rpHRNjmtS9turANIv1GK1ONIO7RfVmmIk/jjTQJU9iJqje9ZSXTSm7rUG4W8q+mWcnACReVChc+9mVZDOb3gUZV1Vs8e7G36nj6XfHw51y1B1lrlnPQJ7U3JdqPz6AG3Je39cR1vnfALxBSpF5QbTHTJOX5ke+sNKo//kDyWWlfzz3rQ== heiko@clove.ch.ic.ac.uk
```

Now log in to the HPC and open (or create) the file '~/.ssh/authorized_keys'.
In a new line at the end of this file, you should add a comment (starting with #) about where that keypair comes from
and then in a second line you should copy and paste the complete contents of your 'id_rsa.pub' file.

```console
#MAC in the office
ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAwRDgM+iQg7OaX/CFq1sZ9jl206nYIhW9SMBqsOIRvGM68/6o6uxZo/D4IlmQI9sAcU5FVNEt9dvDanRqUlC7ZtcOGOCqZsj1HTGD3LcOiPNHYPvi1auEwrXv1hDh4pmJwdgZCRnpewNl+I6RNBiZUyzLzp0/2eIyf4TqG1rpHRNjmtS9turANIv1GK1ONIO7RfVmmIk/jjTQJU9iJqje9ZSXTSm7rUG4W8q+mWcnACReVChc+9mVZDOb3gUZV1Vs8e7G36nj6XfHw51y1B1lrlnPQJ7U3JdqPz6AG3Je39cR1vnfALxBSpF5QbTHTJOX5ke+sNKo//kDyWWlfzz3rQ== heiko@clove.ch.ic.ac.uk
```

Close the 'authorized_keys' file and your connection to the HPC. Now connect again.
You will be asked for the passphrase for your keyfile. Enter it.
You should now be logged in to the HPC. If you are not asked for the passphrase but for the password of your account,
the Server does not accept your key pair.

So far, we have replaced entering the password for your account with entering the passphrase for your keypair.
This is where a so called SSH-agent comes handy. The agent will store your passphrases for you so you do not have
to enter them anymore. Luckily MacOS has one build in, that should have popped up and asked you, whether you want the
agent to take care of your passphrases. If you said 'YES', that was the very last time you ever heard or saw anything of
it or your passphrase. Similar agents exist for more or less every OS. From now on you just have to
enter hostname and username and you are logged in.
