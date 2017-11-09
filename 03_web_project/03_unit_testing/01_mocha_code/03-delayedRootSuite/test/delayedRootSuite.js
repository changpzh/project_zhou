function bootstrap(){
	console.log(new Date() + 'delayedRootSuite');
	setTimeout(run, 1000);
}
bootstrap();