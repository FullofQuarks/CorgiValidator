# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"
  config.vm.box = "digital_ocean"
  config.ssh.private_key_path = "~/.ssh/id_rsa"
  config.vm.define "ubuntu-nichol28-vagrant"
  config.vm.provider :digital_ocean do |provider|
	provider.token = "d85977e978cd8562e4fd5f6efe4b437faba29c47db1d7423e9cff8b66bb8c729"
	provider.image = "ubuntu-18-04-x64"
	provider.region = "nyc3"
	provider.name = "ubuntu-nichol28-vagrant"
	provider.size = "s-1vcpu-1gb"
	provider.monitoring = true
  end

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network "private_network", ip: "192.168.33.10"

  # Setup web server
  config.vm.provision "shell", path: 'install_script.sh', args: '/vagrant', privileged: false
end
