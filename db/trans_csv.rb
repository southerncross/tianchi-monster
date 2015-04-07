#!/bin/ruby

require 'csv'

ROOT_PATH = '/Users/lishunyang/workspace/tianchi-monster/db'
name = 'train_user'

CSV.foreach("#{name}.csv") do |row|
  year, month, day, hour = row[5].split(%r{-|\s})
  puts month
  row[5] = ((month.to_i - 11) * 30 + day.to_i - 18) * 24 + hour.to_i
  CSV.open("#{name}_new.csv", "a") do |csv|
    csv << row
  end
end

File.delete("#{name}.csv")
File.rename("#{name}_new.csv", "#{name}.csv")
