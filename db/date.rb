#!/bin/ruby

while hours = gets.to_i
  day = hours / 24
  month = day > 12 ? 12 : 11
  day = day > 12 ? day - 12 : day + 18
  hour = hours % 24

  print month, "-", day, ":", hour, "\n"
end
