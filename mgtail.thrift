
struct FilterExpression{
1:string name;
2:string exp = '=';
3:string vtype = 'string';
4:string value = '';
}

struct Filter {
1:string collection;
2:string name;
3:list<FilterExpression> exps;
4:map<string, i8> fields = {};
5:map<string, string> formats = {};
6:i32 max_queue_size = 67108864;
7:i32 expried_time = 3600;
}

struct FilterResult {
1:i8 result = 0;
2:string msg = '';
}

struct Log{
1:string collection;
2:string name;
3:string log;
}

service Mgtail{
    FilterResult register_filter(1:Filter filter);
    FilterResult unregister_filter(1:string name);
    Log pull(1:string name);
    list<Filter> get_all_filters();
}