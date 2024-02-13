require 'benchmark'
require 'time'
require 'uri'
def rfc2822_parse(length)
  #attack_str = "A"*length
  #attack_str = "0 Feb 00 00 :00" + " " * length
  #attack_str = "\n"*length
  # '-*-' + '\t'.repeat(54773) + '\t-*-\n\x00-*-'

  #attack_str = "-\*-" + "\t" * length + "\t-\*-\n"
  #puts "-\*-" + "\t" * 1 + "\t-\*-\n"


  #attack_str = 'A'*length + '-*-\r' + '\t'*length + '\x00-*-'*length + '-*-\r--*-\n'

  #attack_str = "A"*length + "-*-\r" + "\t"*length + "\x00-*-"*length + "-*-\r--*-\n"
  #attack_str = "\t"*length

  #attack_str = "\x00" + "--+"*(length) + "\n"
  #attack_str = 'name=Content-Disposition:'*(10955) + 'name="'

  #attack_str = "A\x00" + "zz@\x00z\x00zA@z,\x00"*(27) + "zz"
  #attack_str = "A" + "zz@zzA@z,"*(length) + "zz"

  #attack_str = "zz@z,a,a,a,a"*(length)
  #attack_str = "aaaa@aaa.com"
  #attack_str = "zz@zfefefe;a@a;a@a;a@a"
  #attack_str = "zz@zzz;"+"a@a;"*length
  #attack_str = ARGF.read * length
  attack_str = File.read("attack_str.txt")
  #attack_str = ":\x00"*(length) + ":\n::"
  # ' ' + ' : '.repeat(331) + '\n'

  #attack_str = " " + " : " * length + "\n"
  #puts attack_str
  #puts attack_str
  #/\A[a-zA-Z0-9.!\#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\z/ =~ attack_str
  #/(?:(?:[a-zA-Z\d](?:[-a-zA-Z\d]*[a-zA-Z\d])?)\.)*(?:[a-zA-Z](?:[-a-zA-Z\d]*[a-zA-Z\d])?)\.?/ =~ attack_str
  #/^\s*:?call-seq:(.*?)(^\s*$|\z)/m =~ attack_str
  #/-\*-\s*(.*?\S)\s*-\*-/ =~ attack_str
  # 'A'.repeat(279) + '-*-\r' + '\t'.repeat(279) + '\x00-*-'.repeat(279) + '-*-\r--*-\n'
  #if /\A.*-\*-\s*(.*?\S)\s*-\*-.*\r?\n/ =~ attack_str
  #if /(.*?\S)/ =~ attack_str
  #if /\s*([#*]?)--.*?^\s*(\1)\+\+\n/ =~ attack_str
  #if /;[\r\n\t ]+?([^\x00- ()<>@,;:\\"/\[\]?={}\x7f]+)[\r\n\t ]+?=[\r\n\t ]+?(?:([^\x00- ()<>@,;:\\"/\[\]?={}\x7f]+)|("(?:[\r\n\t !#-\[\]-~\x80-\xff]|\\[\x00-\x7f])*"))/ =~ attack_str
  #if /Content-Disposition:.* name=(?:"(.*?)"|([^;\r\n]*))/ =~ attack_str
  #if /\A(?:[^@,;]+@[^@,;]+(?:\z|[,;]))*\z/ =~ attack_str
  #if /.*::/ =~ attack_str

  regex_str = File.read("regex.txt")
  if (Regexp.new '/poopoo/') =~ "poopoo"
    puts("Passed1")
  end
  if (Regexp.new 'poopoo') =~ "poopoo"
    puts("Passed2")
  end


  if (eval '/poopoo/') =~ "poopoo"
    puts("Passed3")
  end
  #if /^([ ]*)(.+)(?::(?=(?:\s|$)))[ ]?(['"]?)(.*)\3$/ =~ attack_str
  if (Regexp.new regex_str) =~ attack_str
    puts "qqq"
  end
rescue URI::InvalidComponentError
  nil
end

Benchmark.bm do |x|
  #x.report { rfc2822_parse(100) }
  #x.report { rfc2822_parse(1000) }
  #x.report { rfc2822_parse(10000) }
  x.report { rfc2822_parse(100000) }
end