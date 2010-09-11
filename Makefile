PWD=`/bin/pwd`
RUN_DEV_SRV=dev_appserver.py
DEPLOY=appcfg.py

run_test:
	$(RUN_DEV_SRV) $(PWD)

deploy:
	$(DEPLOY) update $(PWD)

updateCron:
	$(DEPLOY) update_cron $(PWD)

cleanDB:
	$(RUN_DEV_SRV) --clear_datastore $(PWD)

clean:
	rm -rf ./*.pyc ./*/*.pyc
