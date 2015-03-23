function drawQr(str){
	var qr = new JSQR();
	var code = new qr.Code();
	code.encodeMode = code.ENCODE_MODE.UTF8_SIGNATURE;
	code.version = code.DEFAULT;
	code.errorCorrection = code.ERROR_CORRECTION.H;
	var input = new qr.Input();
	input.dataType = input.DATA_TYPE.TEXT;
	input.data = {
	     "text": str
	};
	var matrix = new qr.Matrix(input, code);
	var canvas = document.createElement('canvas');
	canvas.setAttribute('width', matrix.pixelWidth);
	canvas.setAttribute('height', matrix.pixelWidth);
	canvas.getContext('2d').fillStyle = 'rgb(0,0,0)';
	matrix.draw(canvas, 0, 0);
	$('#qrcode').html(canvas);
}