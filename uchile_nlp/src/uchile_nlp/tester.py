#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from uchile_nlp import GenerateOrder


while True:
	sens = raw_input('Write your sentence: ')
	# Analize sentence and obtain orders
	if sens=='q':
		break
	s = GenerateOrder(sens)

	# Uncomment for view results
	print sens
	print '==========================='
	print 'Verbs  : {}'.format(s.verbs)
	print 'People : {}'.format(s.people)
	print 'Objects: {}'.format(s.objects)
	print 'Places : {}'.format(s.places)
	print 'Info   : {}'.format(s.information)
	print s.verbs.pop()