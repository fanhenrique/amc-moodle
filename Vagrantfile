# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
# Create a symlink between host and VM
ln -s /vagrant /home/vagrant/amc-testbed

# Check if install.sh is present or someone just copied the Vagrantfile directly
if [[ -f /home/vagrant/classroom-project/install.sh ]]; then
 pushd /home/vagrant/amc-testbed
else
  echo error
fi
./install.sh -qa

SCRIPT

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.provision "shell", privileged: false, inline: $script
  config.vm.provider "virtualbox" do |vb|
    vb.name = "rc_box"
    vb.memory = 2048
    vb.cpus = 2
	vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  end
end

 
Vagrant.configure(2) do |config|
  config.ssh.forward_x11 = true 
end


 