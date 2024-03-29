# Conecta o AMC ao Moodle

### 1. O primeiro passo é instalar as dependências.

Atualizar os repositórios:
```
sudo apt-get update
```
Instalar o gerenciador de janelas:
```
sudo apt-get install -y xorg
```

Instalar o VirtualBox:
```
sudo apt-get insatll -y virtualbox
```

Instalar o Git:
```
sudo apt-get install -y git
```

Instalar o Curl:
```
sudo apt-get install -y curl
```

Instalar o Vagrant:
```
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install vagrant
```


### 2. Em seguida, clone esse repositório
```
git clone https://github.com/fanhenrique/amc-moodle.git
```

### 3. Entre no diretório do repositório
```
cd amc-moodle
```

### 4. Inicie a instalação da máquina virtual (esse passo pode demorar alguns minutos)
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
![copyrigth](https://github.com/fanhenrique/tccAMCMoodle/blob/master/prints/copyrigth.png)

### 9. Confirme as verificações do servidor
![serverchecks1](https://github.com/fanhenrique/tccAMCMoodle/blob/master/prints/serverchecks1.png)
![serverchecks2](https://github.com/fanhenrique/tccAMCMoodle/blob/master/prints/serverchecks2.png)

### 10. Confirme a instalação (esse passo pode demorar alguns minutos)
![installation1](https://github.com/fanhenrique/tccAMCMoodle/blob/master/prints/installation1.png)
![installation2](https://github.com/fanhenrique/tccAMCMoodle/blob/master/prints/installation2.png)

### 11. Criar uma conta de administrador (altere apenas os campos *New password* e *e-mail address*), em seguida clique em *Update Profile*
Recomenda-se utilizar a mesma senha e endereço de e-mail
![admin1](https://github.com/fanhenrique/tccAMCMoodle/blob/master/prints/admin1.png)
![admin2](https://github.com/fanhenrique/tccAMCMoodle/blob/master/prints/admin2.png)

### 12. Configure um nome para a página, localização(America/Sao_paulo) e a configuração de e-mail de saída. Salve as mudanças
![settings1](https://github.com/fanhenrique/tccAMCMoodle/blob/master/prints/settings1.png) 
![settings2](https://github.com/fanhenrique/tccAMCMoodle/blob/master/prints/settings2.png)

# *Moodle* e o *Auto Multiple Choice* estão prontos para serem usados
Para testar o AMC use o comando:
```
auto-multiple-choice
```

## Caso alguma etapa falhe use o comando, e inicie o processo a partir do passo 4
```
vagrant destroy
```



