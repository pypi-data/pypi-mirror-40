#! /usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb

def search():
	db = getDb(True)
	cursor = db.cursor()

	sql = "select aid from author_whitelist" #work_blacklist"

	cursor.execute(sql)

	print(cursor.fetchall())

	db.close()


def getDb(isTest):
	path = "rm-bp12bzgmvo85rflhio.mysql.rds.aliyuncs.com" if isTest else "rm-bp10b4n5116u90h5t.mysql.rds.aliyuncs.com"
	username = "migration_test" if isTest else "webuser"
	password = "migrationTest*" if isTest else "fnwkufkljfk984ewJ"
	dbName = "idl_night" if isTest else "db_nt_operations"
	return MySQLdb.connect(path, username, password, dbName, charset='utf8')