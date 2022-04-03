import config
import sqlite3
import re

keyList = ["TypeScript", "Ruby", "Elixir", "Python", "Javascript", "C++", "C#", "HTML", "CSS", "PHP", "SQL", "JSON", " AWS", "Azure", "Bash", "XML", "jQuery", "Bootstrap", "TWIG", "Blade", "Docker", "Kubernetes", "OpenShift", "Ansible", "Terraform", "Jenkins", "Prometheus", "SharePoint", "Tempest", " Unity", "Django", "Postgres", "GCP", "Angular", "React", "Kotlin", "Swift", "Figma"]

def FindKeywords():

	conn = sqlite3.connect('jobdb.sqlite')

	cur = conn.cursor()

	cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Keywords' ''')

	if(cur.fetchone()[0] == 0):
		cur.execute(''' CREATE TABLE Keywords (jobs_id INTEGER DEFAULT 0 UNIQUE, TypeScript INTEGER DEFAULT 0, Ruby INTEGER DEFAULT 0, Elixir INTEGER DEFAULT 0, Python INTEGER DEFAULT 0, Javascript INTEGER DEFAULT 0, CPlusPlus INTEGER DEFAULT 0, CSharp INTEGER DEFAULT 0, HTML INTEGER DEFAULT 0, CSS INTEGER DEFAULT 0, PHP INTEGER DEFAULT 0, SQL INTEGER DEFAULT 0, JSON INTEGER DEFAULT 0, AWS INTEGER DEFAULT 0, Azure INTEGER DEFAULT 0, Bash INTEGER DEFAULT 0, XML INTEGER DEFAULT 0, jQuery INTEGER DEFAULT 0, Bootstrap INTEGER DEFAULT 0, TWIG INTEGER DEFAULT 0, Blade INTEGER DEFAULT 0, Docker INTEGER DEFAULT 0, Kubernetes INTEGER DEFAULT 0, OpenShift INTEGER DEFAULT 0, Ansible INTEGER DEFAULT 0, Terraform INTEGER DEFAULT 0, Jenkins INTEGER DEFAULT 0, Prometheus INTEGER DEFAULT 0, SharePoint INTEGER DEFAULT 0, Tempest INTEGER DEFAULT 0, Unity INTEGER DEFAULT 0, Django INTEGER DEFAULT 0, Postgres INTEGER DEFAULT 0, GCP INTEGER DEFAULT 0, Angular INTEGER DEFAULT 0, React INTEGER DEFAULT 0, Kotlin INTEGER DEFAULT 0, Swift INTEGER DEFAULT 0, Figma INTEGER DEFAULT 0) ''')

	conn.commit()
	jobTuple = cur.execute(''' SELECT id, description FROM Jobs ''').fetchall()


	for id, description in jobTuple:
		
		if cur.execute(''' SELECT jobs_id FROM Keywords WHERE jobs_id = ? ''', (id, )).fetchone():
			pass
		else:
			cur.execute(''' INSERT INTO Keywords (jobs_id) VALUES (?) ''', (id, ))
		if description != None:
			for keyword in keyList:
				if keyword == "React":
					if keyword in description:
						cur.execute(f"UPDATE Keywords SET {keyword} = 1 WHERE jobs_id = ?", (id,))
					else:
						cur.execute(f"UPDATE Keywords SET {keyword} = 0 WHERE jobs_id = ?", (id,))
				else:
					if keyword.lower() in description.lower():
						if keyword == " AWS":
							keyword = "AWS"
						elif keyword == "C#":
							keyword = "CSharp"
						elif keyword == "C++":
							keyword = "CPlusPlus"
						elif keyword == " Unity":
							keyword = "Unity"
						cur.execute(f"UPDATE Keywords SET {keyword} = 1 WHERE jobs_id = ?", (id,))
					else:
						if keyword == " AWS":
							keyword = "AWS"
						elif keyword == "C#":
							keyword = "CSharp"
						elif keyword == "C++":
							keyword = "CPlusPlus"
						elif keyword == " Unity":
							keyword = "Unity"
						cur.execute(f"UPDATE Keywords SET {keyword} = 0 WHERE jobs_id = ?", (id,))
			conn.commit()
	conn.commit()

def CountKeywords():
	conn = sqlite3.connect('jobdb.sqlite')
	cur = conn.cursor()

	for keyword in keyList:
		if keyword == " AWS":
			keyword = "AWS"
		elif keyword == "C++":
			keyword = "CPlusPlus"
		elif keyword == "C#":
			keyword = "CSharp"
		elif keyword == " Unity":
			keyword = "Unity"
		keywordCount = cur.execute(f"SELECT Count() FROM Keywords WHERE {keyword} = 1").fetchone()[0]
		if cur.execute(''' SELECT date FROM Metadata WHERE date = date('now', 'localtime') ''').fetchone():
			cur.execute(f"UPDATE Metadata SET date = date('now', 'localtime'), {keyword} = ? WHERE date = date('now', 'localtime')", (keywordCount,))
		else:
			cur.execute(f"INSERT INTO Metadata (date, {keyword}) VALUES (date('now', 'localtime'), ?)", (keywordCount,))
	conn.commit()

	