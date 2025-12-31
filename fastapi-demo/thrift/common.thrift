/**
 * Common Thrift IDL
 * 定义通用类型和结构
 */

namespace py app.thrift.common

/**
 * 通用分页请求
 */
struct PaginationRequest {
    1: required i32 page = 1,
    2: required i32 page_size = 20,
}

/**
 * 通用分页响应元数据
 */
struct PaginationMeta {
    1: required i32 total,
    2: required i32 page,
    3: required i32 page_size,
    4: required i32 total_pages,
    5: required bool has_next,
    6: required bool has_prev,
}

/**
 * 通用响应包装
 */
struct Response {
    1: required i32 code,
    2: required string message,
    3: optional string data,  // JSON 字符串
}

/**
 * 排序方向
 */
enum SortOrder {
    ASC = 0,
    DESC = 1,
}

/**
 * 排序参数
 */
struct SortParam {
    1: required string field,
    2: required SortOrder order = SortOrder.DESC,
}

/**
 * 时间范围
 */
struct TimeRange {
    1: optional string start_time,
    2: optional string end_time,
}

/**
 * 通用异常
 */
exception ValidationException {
    1: string message,
    2: optional map<string, string> errors,
}

exception NotFoundException {
    1: string message,
    2: optional string resource_type,
    3: optional string resource_id,
}

exception UnauthorizedException {
    1: string message,
}

exception ForbiddenException {
    1: string message,
}

exception InternalException {
    1: string message,
}
