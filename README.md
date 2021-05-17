# tccAMCMoodle

### 1. O primeiro passo é instalar as dependências.

Atualizar os repositórios:
```
sudo apt-get update
```

Instalar o VirtualBox:
```
sudo apt-get insatll -y virtualbox
```

Instalar o Git:
```
sudo apt-get install -y git
```

Instalar o Vagrant:
```
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install vagrant
```


### 2. Em seguida, clone esse repositório
```
git clone https://github.com/fanhenrique/tccAMCMoodle.git
```

### 3. Entre no diretório do repositório
```
cd tccAMCMoodle
```

### 4. Inicie a instalação da máquina virtual
```
vagrant up
```

### 5. Para acessar a máquina virtual
```
vagrant ssh
```

### 6. Abra no navegador Firefox que já está instalado na máquina
```
firefox
```

### 7. Acesse *localhost/moodle*

### 8. Confirme os direitos autorais



