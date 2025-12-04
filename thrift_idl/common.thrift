/**
 * Common Thrift definitions
 * 通用 Thrift 定义
 */

namespace py common

/**
 * 响应状态码
 */
enum StatusCode {
    SUCCESS = 200,
    CREATED = 201,
    BAD_REQUEST = 400,
    NOT_FOUND = 404,
    INTERNAL_ERROR = 500
}

/**
 * 通用响应结构
 */
struct Response {
    1: required i32 code,
    2: required string message,
    3: optional string data
}

/**
 * 分页参数
 */
struct PaginationParams {
    1: required i32 skip = 0,
    2: required i32 limit = 100
}

/**
 * 分页响应
 */
struct PaginatedResponse {
    1: required i32 total,
    2: required list<string> items,
    3: optional i32 skip,
    4: optional i32 limit
}

/**
 * 基础异常
 */
exception ServiceException {
    1: required i32 code,
    2: required string message,
    3: optional string details
}
