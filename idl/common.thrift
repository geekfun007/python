/**
 * 通用数据类型定义
 * Common data types and structures
 */

namespace py app.thrift_gen.common

/**
 * 错误码枚举
 */
enum ErrorCode {
    SUCCESS = 0,                    // 成功
    UNKNOWN_ERROR = 1,              // 未知错误
    INVALID_PARAMS = 100,           // 参数无效
    UNAUTHORIZED = 101,             // 未授权
    FORBIDDEN = 102,                // 禁止访问
    NOT_FOUND = 103,                // 资源未找到
    CONFLICT = 104,                 // 资源冲突
    VALIDATION_ERROR = 105,         // 验证错误
    DATABASE_ERROR = 200,           // 数据库错误
    CACHE_ERROR = 201,              // 缓存错误
    INTERNAL_ERROR = 500,           // 内部错误
}

/**
 * 基础响应结构
 */
struct BaseResponse {
    1: required i32 code,           // 响应码
    2: required string message,     // 响应消息
    3: optional string request_id,  // 请求ID
}

/**
 * 分页请求参数
 */
struct PaginationRequest {
    1: required i32 page = 1,       // 页码，从1开始
    2: required i32 page_size = 20, // 每页数量
    3: optional string order_by,    // 排序字段
    4: optional bool order_desc,    // 是否降序
}

/**
 * 分页响应信息
 */
struct PaginationInfo {
    1: required i32 page,           // 当前页码
    2: required i32 page_size,      // 每页数量
    3: required i64 total,          // 总数量
    4: required i32 pages,          // 总页数
}

/**
 * 时间范围查询
 */
struct TimeRange {
    1: optional i64 start_time,     // 开始时间戳（毫秒）
    2: optional i64 end_time,       // 结束时间戳（毫秒）
}
