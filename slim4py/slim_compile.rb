# frozen_string_literal: true

# Author => Adriano Romanazzo
# Copyright => Copyright 2019, Adriano Romanazzo (https://github.com/multiversecoder)
# LICENSE => MIT
# Maintainer => https://github.com/multiversecoder
# Status => Production
#
# This script takes arguments through shells and returns
# a perfectly rendered template using Ruby and Slim
#
# ARGV USED:
#  ARGV[0] = the default include_dir for template lookup
#  ARGV[1] = the absolute path of the template (including the filename)
#  ARGV[2] = the name of the temp json file that contains all the arguments
#
# NOTE
#  do not set pretty options to true,
#  because if true make the process too slow!

require 'json'

require 'slim'
require 'slim/include'

Slim::Engine.set_options shortcut: {
  '&' => { tag: 'input', attr: 'type' },
  '#' => { attr: 'id' },
  '.' => { attr: 'class' }
}, include_dirs: ["#{ARGV[0]}/"], sort_attrs: false

begin
    kwargs = JSON.parse(File.read(ARGV[2])).inject({}) { |kwargs, (k, v)| kwargs [k.to_sym] = v; kwargs }
    if ARGV[1].include? "/tmp/tmp"
      tpl = Slim::Template.new(ARGV[1]).render(Object.new, kwargs)
    else
      tpl = Slim::Template.new("#{ARGV[0]}/#{ARGV[1]}").render(Object.new, kwargs)
    end
rescue StandardError => e
  puts "#<Slim_Error_for_python>: #{e}"
else
  puts tpl
  exit
end

