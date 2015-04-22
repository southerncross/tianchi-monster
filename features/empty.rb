#!/bin/ruby
# -*- coding: utf-8 -*-

# raw data format: <uid,iid,hours>
def readRaw
  puts "Reading raw data.."
  # data = {uid => {iid => [hour1, hour2, ...]}}}
  data = {}
  while line = $stdin.gets do
    uid, iid, hour = line.chomp.split(',').map {|e| e.to_i}
    data[uid] = {} unless data.key?(uid)
    data[uid][iid] = [] unless data[uid].key?(iid)
    data[uid][iid] += [hour]
  end
  data.each_pair do |u, ihs|
    ihs.each_key {|i| ihs[i].uniq.sort}
  end
  return data
end

def extractUserEmptyItvFeatures(data)
  # user_empty_itvs = {uid => [itv1, itv2, ...]}
  user_empty_itvs = {}
  data.each_pair do |u, ihs|
    ihs.each_pair do |i, hs|
      itvs = hs.length > 1 ? hs.each_cons(2).map {|a, b| b - a} : [hs[0]]
      user_empty_itvs[u] = [] unless user_empty_itvs.key?(u)
      user_empty_itvs[u] += itvs
    end
  end
  # user_empty_itv_features = {uid => {:median => X, :average => Y, :variance => Z}}
  user_empty_itv_features = {}
  user_empty_itvs.each_pair do |u, itvs|
    user_empty_itv_features[u] = {}
    sorted = itvs.sort
    len = itvs.length
    user_empty_itv_features[u][:median] = (sorted[(len - 1) / 2] + sorted[len / 2]) / 2.0
    user_empty_itv_features[u][:average] = sorted.reduce(:+).to_f / len
    user_empty_itv_features[u][:variance] = sorted.inject(0) {|v, e| v + (e - user_empty_itv_features[u][:average]) ** 2}
  end
  return user_empty_itv_features
end

def extractUserItemEmptyItvFeatures(data)
  # user_item_empty_itvs = {uid => {iid => [itv1, itv2, ...]}}
  user_item_empty_itvs = {}
  data.each_pair do |u, ihs|
    ihs.each_pair do |i, hs|
      itvs = hs.length > 1 ? hs.each_cons(2).map {|a, b| b - a} : [hs[0]]
      user_item_empty_itvs[u] = {} unless user_item_empty_itvs.key?(u)
      user_item_empty_itvs[u][i] = itvs
    end
  end
  # user_item_empty_itv_features = {uid => {iid => {:median => X, :average => Y, :variance => Z}}}
  user_item_empty_itv_features = {}
  user_item_empty_itvs.each_pair do |u, iitvs|
    user_item_empty_itv_features[u] = {}
    iitvs.each_pair do |i, itvs|
      user_item_empty_itv_features[u][i] = {}
      sorted = itvs.sort
      len = itvs.length
      user_item_empty_itv_features[u][i][:median] = (sorted[(len - 1) / 2] + sorted[len / 2]) / 2.0
      user_item_empty_itv_features[u][i][:average] = sorted.reduce(:+).to_f / len
      user_item_empty_itv_features[u][i][:variance] = sorted.inject(0) {|v, e| v + (e - user_item_empty_itv_features[u][i][:average]) ** 2}
    end
  end
  return user_item_empty_itv_features
end

def writeUserEmptyItvFeatures(name, user_empty_itv_features)
  file = File.open(name, "w")
  user_empty_itv_features.each_pair do |u, fs|
    file.puts(([u] + fs.values).join(','))
  end
end

def writeUserItemEmptyItvFeatures(name, user_item_empty_itv_features)
  file = File.open(name, "w")
  user_item_empty_itv_features.each_pair do |u, ifs|
    ifs.each_pair do |i, fs|
      file.puts(([u, i] + fs.values).join(','))
    end
  end
end

user_feature = ARGV[0]
user_item_feature = ARGV[1]

data = readRaw
writeUserEmptyItvFeatures(user_feature, extractUserEmptyItvFeatures(data))
writeUserItemEmptyItvFeatures(user_item_feature, extractUserItemEmptyItvFeatures(data))
