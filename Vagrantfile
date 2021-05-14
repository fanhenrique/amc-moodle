# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
# Create a symlink between host and VM
ln -s /vagrant /home/vagrant/amc-testbed

# Check if install.sh is present or someone just copied the Vagrantfile directly
if [[ -f /home/vagrant/amc-testbed/installAmcMoodle.sh ]]; then
 pushd /home/vagrant/amc-testbed
else
  echo error
fi
./installAmcMoodle.sh -dams

SCRIPT

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.provision "shell", privileged: false, inline: $script
  config.vm.provider "virtualbox" do |vb|
    vb.name = "amc_moodle"
    vb.memory = 2048
    vb.cpus = 2
	vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  end
end

 
Vagrant.configure(2) do |config|
  config.ssh.forward_x11 = true 
end


 