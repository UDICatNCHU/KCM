#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
with open('time.log', 'r', encoding='utf-8') as f:
    time = [ int(i.split(':')[1]) for i in f]
    duration = time[1]-time[0]
with open('time.log', 'a', encoding='utf-8') as f:
    f.write("Run time : "+str(datetime.timedelta(seconds=duration)) + "\n")
