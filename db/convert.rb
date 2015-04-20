#!/bin/ruby

name = ARGV[0]

file = File.open(name, "w")

print " converting...\n"

while line = $stdin.gets do
  row = line.chomp.split(',')
  year, month, day, hour = row[5].split(%r{-|\s})
  row[5] = ((month.to_i - 11) * 30 + day.to_i - 18) * 24 + hour.to_i
  file.print row.join(","), "\n"
end

file.close

print "convert completed!\n"
