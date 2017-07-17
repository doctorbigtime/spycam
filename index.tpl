<html>
<head>
</head>
<body>
Available:
<ul>
% for item in subdirs:
    <li>{{curr_dir}}<a href="/index/{{curr_dir}}{{item}}/">{{item}}</a></li>
% end
</ul>
</body>
</html>

