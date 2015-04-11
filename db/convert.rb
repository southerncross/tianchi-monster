#!/bin/ruby

name = ARGV[0]

def clean
  puts "\e[H\e[2J";
end

def emoji()
  print [127740 + rand(1000)].pack('U*');
end

file = File.open(name, "w")

print emoji(), " converting...\n"

while line = $stdin.gets do
  row = line.chomp.split(',')
  year, month, day, hour = row[5].split(%r{-|\s})
  row[5] = ((month.to_i - 11) * 30 + day.to_i - 18) * 24 + hour.to_i
  file.print row.join(","), "\n"
end

file.close

print emoji(), " convert completed!\n"
