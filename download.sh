#!/usr/bin/bash
curl https://www.asx.com.au/data/trt/ib_expectation_curve_graph.pdf | python -c 'import sys,hashlib;open(f"pdfs/{hashlib.sha256(d:=sys.stdin.buffer.read()).hexdigest()}.pdf","wb").write(d)'
