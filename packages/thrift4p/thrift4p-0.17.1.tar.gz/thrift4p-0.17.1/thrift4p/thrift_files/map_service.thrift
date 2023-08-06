namespace java com.didapinche.map.thrift

struct TPoint {
    1: double lon;
    2: double lat;
}

struct TLine {
    1: TPoint startPoint;
    2: TPoint endPoint;
    3: i64 id;
}

struct TResult {
    1: i16 code;  // 0-success else-fail
    2: string msg;
    3: map<i64, i32> distances;  // key-lineId value-distance
}

struct TDistrictResult {
    1: i16 code;  // 0-success else-fail
    2: string msg;
    3: i32 cityId;
    4: i32 districtId;
}

service MapService{
    i32 getCityId(1:double lon, 2:double lat)
    i32 getDistance(1:double slon, 2:double slat, 3:double elon, 4:double elat)
    list<i32> getDistances(1:i32 cityId, 2:list<string> params)
    TResult getBatchDistance(1:list<TLine> lines)
    TDistrictResult getDistrictId(1:double lon, 2:double lat, 3:i32 possibleCityId)
}