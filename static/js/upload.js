$(document).ready(function() {
	var obj = $("#dragandrophandler");
	var fileInput=$('#file-upload');
	var statusbarObj=$('#statusbar');
	fileInput.on('change', function(e) {
		e.preventDefault();
		var files =  e.target.files;	
		handleFileUpload(files, statusbarObj);
	});
	obj.on('click', function(e) {
		$('#file-upload').trigger('click');
	});
	obj.on('dragenter', function(e) {
		e.stopPropagation();
		e.preventDefault();
		$(this).css('border', '2px solid #0B85A1');
	});
	obj.on('dragover', function(e) {
		e.stopPropagation();
		e.preventDefault();
	});
	obj.on('drop', function(e) {

		$(this).css('border', '2px dotted #0B85A1');
		e.preventDefault();
		var files = e.originalEvent.dataTransfer.files;	

		//We need to send dropped files to Server
		handleFileUpload(files, statusbarObj);
	});
	$(document).on('dragenter', function(e) {
		e.stopPropagation();
		e.preventDefault();
	});
	$(document).on('dragover', function(e) {
		e.stopPropagation();
		e.preventDefault();
		obj.css('border', '2px dotted #0B85A1');
	});
	$(document).on('drop', function(e) {
		e.stopPropagation();
		e.preventDefault();
	});

});
function sendFileToServer(formData, status) {
	var uploadURL = "/upload-file"; //Upload URL
	var extraData = {}; //Extra Data.
	var jqXHR = $.ajax({
		xhr : function() {
			var xhrobj = $.ajaxSettings.xhr();
			if (xhrobj.upload) {
				xhrobj.upload.addEventListener('progress', function(event) {
					var percent = 0;
					var position = event.loaded || event.position;
					var total = event.total;
					if (event.lengthComputable) {
						percent = Math.ceil(position / total * 100);
					}
					//Set progress
					status.setProgress(percent);
				}, false);
			}
			return xhrobj;
		},
		url : uploadURL,
		type : "POST",
		contentType : false,
		processData : false,
		cache : false,
		data : formData,
		success : function(data) {
			status.setProgress(100);

			$("#status1").append("File upload Done<br>");
		}
	});

	status.setAbort(jqXHR);
}

function createStatusbar(obj) {
	this.statusbar = $("<div class='statusbar'></div>");
	this.filename = $("<div class='filename'></div>").appendTo(this.statusbar);
	this.size = $("<div class='filesize'></div>").appendTo(this.statusbar);
	this.progressBar = $("<div class='progressBar'><div></div></div>")
			.appendTo(this.statusbar);
	this.abort = $("<div class='abort'>Abort</div>").appendTo(this.statusbar);
	//obj.after(this.statusbar);
	obj.html(this.statusbar);

	this.setFileNameSize = function(name, size) {
		var sizeStr = "";
		var sizeKB = size / 1024;
		if (parseInt(sizeKB) > 1024) {
			var sizeMB = sizeKB / 1024;
			sizeStr = sizeMB.toFixed(2) + " MB";
		} else {
			sizeStr = sizeKB.toFixed(2) + " KB";
		}

		this.filename.html(name);
		this.size.html(sizeStr);
	}
	this.setProgress = function(progress) {
		var progressBarWidth = progress * this.progressBar.width() / 100;
		this.progressBar.find('div').animate({
			width : progressBarWidth
		}, 10).html(progress + "% ");
		if (parseInt(progress) >= 100) {
			this.abort.hide();
		}
	}
	this.setAbort = function(jqxhr) {
		var sb = this.statusbar;
		this.abort.click(function() {
			jqxhr.abort();
			sb.hide();
		});
	}
}
function endsWith(str) {
    return str.indexOf(".xls", str.length - ".xls".length) !== -1 || str.indexOf(".xlsx", str.length - ".xlsx".length) !== -1;
}
function handleFileUpload(files, obj) {
	if(files.length > 1){
		alert("Nhiều quá thở không kịp ! Một file thôi.");
		return;
	}
//	if(!endsWith(files[0].name)){
//		alert("File không phải là excel.");
//		return;
//	}
	//for (var i = 0; i < files.length; i++) {
		var fd = new FormData();
		fd.append('file', files[0]);

		var status = new createStatusbar(obj); //Using this we can set progress.
		status.setFileNameSize(files[0].name, files[0].size);
		sendFileToServer(fd, status);
	//}
}
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
	$('#qrcode').append(canvas);
}

