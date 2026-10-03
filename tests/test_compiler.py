from app.domain import Plan
from app.compiler import compile_plan
def test_compile():
 p=Plan.model_validate({"objective":"x","steps":[{"key":"a","agent":"sales","capability":"x"},{"key":"b","agent":"supervisor","capability":"y","kind":"evaluate","depends_on":["a"]}]})
 assert list(compile_plan(p).nodes)==["a","b"]
