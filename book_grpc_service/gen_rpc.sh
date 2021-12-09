# gen python protos code path
target_p='book_grpc_service'
# project proto path
source_p='protos'
# service
service_list=("manager" "social")

mkdir -p $target_p
rm -r "${target_p:?}/${source_p:?}"*

for service in "${service_list[@]}"
do
  echo  "from proto file:" $source_p/$service.proto "gen proto py file to" $target_p/$source_p
  poetry run python -m grpc_tools.protoc \
    --mypy_grpc_out=./$target_p \
    --mypy_out=./$target_p \
    --python_out=./$target_p \
    --grpc_python_out=./$target_p \
    -I. \
    $source_p/$service.proto
done

touch $target_p/$source_p/__init__.py
# fix grpc tools bug
sed -i 's/from protos import/from . import/' $target_p/$source_p/*.py
