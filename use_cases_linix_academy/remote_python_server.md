### Visial Studio Code use remote python server

> Install all ssh-remote plugins to your Visual Studio Code

> Copy ssh-key
ssh-copy-id -i ~/.ssh/id_rsa.pub vagrant@192.168.0.13

> Create ssh config

```
 Host python-server
    HostName 192.168.0.13
    User vagrant
    IdentityFile ~/.ssh/id_rsa-remote-ssh

```   

> Open a remote window > Remote SSH > Add new SSH host